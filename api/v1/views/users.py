#!/usr/bin/python3
"""
User objects that handles all default RESTFul API actions:
"""
from models.user import User
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ status view function """
    my_users = storage.all(User)
    users_list = []
    for user in my_users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def user_id(user_id=None):
    """ status view function """
    user_key = "User.{}".format(user_id)
    my_users = storage.all(User)
    try:
        my_user = my_users[user_key]
        return jsonify(my_user.to_dict())
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id=None):
    """ status view function """
    user_key = "User.{}".format(user_id)
    my_users = storage.all(User)
    if user_key in my_users:
        my_user = my_users[user_key]
        storage.delete(my_user)
        storage.save()
        dict_empty = {}
        return make_response(jsonify(dict_empty), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """ status view function """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "email" not in request.get_json():
        abort(400, description="Missing email")
    if "password" not in request.get_json():
        abort(400, description="Missing password")
    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def user_put(user_id=None):
    """ status view function """
    user_key = "User.{}".format(user_id)
    my_objs = storage.all(User)
    my_obj = my_objs[user_key]
    if user_key not in my_objs:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(my_obj, k, v)
    my_obj.save()
    return make_response(jsonify(my_obj.to_dict()), 200)
