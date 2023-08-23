#!/usr/bin/python3
"""Route for the State objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request
import json
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def states():
    """return the list of all State objects"""
    list_obj = []
    dict_storage = storage.all(State)

    for key, value in dict_storage.items():
        list_obj.append(value.to_dict())
    return jsonify(list_obj)


@app_views.route("/states/<id>", strict_slashes=False)
def state_id(id):
    """return state for the id"""
    obj = storage.get(State, id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route("/states/<id>", methods=["DELETE"], strict_slashes=False)
def delete_state(id):
    """delete a state by id"""
    obj = storage.get(State, id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def post_state():
    """add a state with the name, mandatory"""
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        return jsonify(error="Not a JSON"), 400

    obj = State()

    try:
        obj.name = data["name"]
    except KeyError:
        return jsonify(error="Missing name"), 400

    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<id>", methods=["PUT"], strict_slashes=False)
def put_state(id):
    """PUT method with the id"""
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        return jsonify(error="Not a JSON"), 400

    obj = storage.get(State, id)
    if obj is None:
        abort(404)

    for key, value in data.items():
        if key not in ["id", "created", "updated_at"]:
            setattr(obj, key, value)

    storage.save()
    return jsonify(obj.to_dict()), 200
