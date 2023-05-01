#!/usr/bin/python3
"""a blueprint module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def get_post(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'user_id' not in request.get_json():
            abort(400, 'Missing user_id')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        if not storage.get(User, request.get_json()['user_id']):
            abort(404)
        json_data = request.get_json()
        place = Place(user_id=json_data['user_id'], name=json_data['name'])
        place.city_id = city_id
        place.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def all_methods(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        for key, value in request.get_json().items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)
