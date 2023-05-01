#!/usr/bin/python3
"""a blueprint module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict for city in state.cities])