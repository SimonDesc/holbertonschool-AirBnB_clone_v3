#!/usr/bin/python3
"""Users objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users():
    """List all User object into a valid JSON"""
    list_obj = []
    dict_storage = storage.all(User)

    for key, value in dict_storage.items():
        list_obj.append(value.to_dict())
    return jsonify(list_obj)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def users_id(user_id):
    """Retrieves a User object by his id"""
    obj_user_id = storage.get(User, user_id)
    if obj_user_id is None:
        abort(404)
    return jsonify(obj_user_id.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def users_delete(user_id):
    """Delete a User object by his id"""
    empty = {}
    obj_user_id = storage.get(User, user_id)
    if obj_user_id is None:
        abort(404)
    storage.delete(obj_user_id)
    storage.save()
    return (jsonify(empty), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_create():
    """Returns the new User with the status code 201"""
    data = request.get_json()
    if data is None:
        return "Not a JSON\n", 400
    elif "email" not in data:
        return "Missing email\n", 400
    elif "password" not in data:
        return "Missing password\n", 400
    else:
        obj = User()
        obj.email = data["email"]
        obj.password = data["password"]
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def users_update(user_id):
    """Update a User object by his id"""
    obj_update = storage.get(User, user_id)
    if obj_update is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON\n", 400
        else:
            for key, value in data.items():
                if key not in ["id", "email", "created_at", "updated_at"]:
                    setattr(obj_update, key, value)
            storage.save()

        return jsonify(obj_update.to_dict()), 200
