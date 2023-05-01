#!/usr/bin/python3
"""a blueprint module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities',
strict_slashes=False, methods=['GET'])
def cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict for city in state.cities])


@app_views.route('/api/v1/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonifyL(city.to_dict())


@app_views('/api/v1/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views('/api/v1/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if request.get_json:
        if not state:
            abort(404)
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        json_data = request.get_json()
        city = City(name=json_data['name'])
        storage.new(city)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views('/api/v1/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.get_json():
        if not request.get_json():
            abort(400, 'Not a JSON')
        for key, value in request.json.items():
            if key not in ['state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
