#!/usr/bin/python3
"""
City objects that handles all default RESTFul API actions:
"""
from models.state import State
from models.city import City
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id=None):
    """ status view function """
    state_key = "State.{}".format(state_id)
    my_objs = storage.all(State)
    city_list = []
    try:
        my_state = my_objs[state_key]
        my_cities = my_state.cities
        for city in my_cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id=None):
    """ status view function """
    city_key = "City.{}".format(city_id)
    my_objs = storage.all(City)
    try:
        my_city = my_objs[city_key]
        return jsonify(my_city.to_dict())
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id=None):
    """ status view function """
    city_key = "City.{}".format(city_id)
    my_objs = storage.all(City)
    if city_key in my_objs:
        my_city = my_objs[city_key]
        storage.delete(my_city)
        storage.save()
        dict_empty = {}
        return make_response(jsonify(dict_empty), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_post(state_id=None):
    """ status view function """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    new_city = City()
    new_city.state_id = state_id
    new_city.name = request.get_json().get('name')
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id=None):
    """ status view function """
    city_key = "City.{}".format(city_id)
    my_objs = storage.all(City)
    my_obj = my_objs[city_key]
    if city_key not in my_objs:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(my_obj, k, v)
    my_obj.save()
    return make_response(jsonify(my_obj.to_dict()), 200)