#!/usr/bin/python3
"""a blueprint module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.amenity import Amenity

@app_views.route('/api/v1/amenities', strict_slashes=False, methods=['GET'])
def amenities():
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/api/v1/amenities/<amenity_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def amenity_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        for key, value in request.json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route('/api/v1/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    json_data = request.get_json()
    amenity = Amenity(name=json_data['name'])
    storage.new(amenity)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)
