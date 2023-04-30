#!/usr/bin/python3
"""a blueprint module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    return jsonify([state.to_dict()
                   for state in storage.all(State).values()])


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state_object(state_id):
    if storage.get(State, state_id) is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    
