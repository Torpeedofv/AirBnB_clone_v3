#!/usr/bin/python3
"""a blueprint module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """returns a list of all the state objects"""
    return jsonify([state.to_dict()
                   for state in storage.all(State).values()])


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state_object(state_id):
    if storage.get(State, state_id) is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def post_put(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post():
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    json_date = request.get_json()
    state = State(name=json_date['name'])
    storage.new(state)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)
