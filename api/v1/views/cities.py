#!/usr/bin/python3
"""Route for the State objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request
import json
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)

    """Get the list of cities associated with the State object"""
    city_list = obj_state.cities

    city_dicts = []
    """Convert each city to a dictionary"""
    for city in city_list:
        city_dicts.append(city.to_dict())

    return jsonify(city_dicts), 200


@app_views.route("/cities/<id>", strict_slashes=False)
def city_id(id):
    """return city for the id"""
    obj = storage.get(City, id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route("/cities/<id>", methods=["DELETE"], strict_slashes=False)
def delete_city(id):
    """delete a city by id"""
    obj = storage.get(City, id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """add a city with the name and the state id"""
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return "Not a JSON\n", 400
    elif "name" not in data:
        return "Missing name\n", 400
    else:
        obj = City()
        obj.name = data["name"]
        obj.state_id = state_id
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """PUT method with the id"""

    obj = storage.get(City, city_id)

    if obj is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON\n", 400
        for key, value in data.items():
            if key not in ["id", "created", "updated_at"]:
                setattr(obj, key, value)

        storage.save()
        return jsonify(obj.to_dict()), 200
