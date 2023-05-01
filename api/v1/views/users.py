#!/usr/bin/python3
"""a blueprint module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/api/v1/users', strict_slashes=False, methods=['GET', 'POST'])
def post_get():
    users = storage.all(User)
    if request.method == 'GET':
        return jsonify([user.to_dict() for user in users.values()])
    
    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'email' not in request.get_json:
            abort(400, 'Missing email')
        if 'password' not in request.get_json:
            abort(400, 'Missing password')
        json_data = request.get_json()
        user = User(password=json_data['password'], email=json_data['email'])
        storage.new(user)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/api/v1/users/<user_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def methods(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not JSON')
        for key, value in request.json.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        return make_response(jsonify(user.to_dict()), 200)
