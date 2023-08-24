#!/usr/bin/python3
"""Route for the Place objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def places(city_id):
    """Retrieves the list of all City objects of a State"""
    obj_state = storage.get(City, city_id)
    if obj_state is None:
        abort(404)

    """Get the list of place associated with the State object"""
    place_list = obj_state.places

    place_dicts = []
    """Convert each city to a dictionary"""
    for city in place_list:
        place_dicts.append(city.to_dict())

    return jsonify(place_dicts), 200


@app_views.route("/places/<id>", strict_slashes=False)
def get_places_by_id(id):
    """retrive an place by id"""
    obj = storage.get(Place, id)

    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/places/<id>", methods=["DELETE"], strict_slashes=False)
def delete_place(id):
    """delete a place by id"""

    obj = storage.get(Place, id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new Place and return it with status code 201"""

    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user_id = data["user_id"]
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    obj_place = Place()
    obj_place.name = data["name"]
    obj_place.city_id = city_id
    obj_place.user_id = user_id
    storage.new(obj_place)
    storage.save()

    return jsonify(obj_place.to_dict()), 201


@app_views.route("/places/<id>", methods=["PUT"], strict_slashes=False)
def update_place(id):
    """Update a Place and return it with status code 201"""
    obj = storage.get(Place, id)

    if obj is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON\n", 400
        for key, value in data.items():
            if key not in ["id", "user_id", "city_id", "created_at",
                           "updated_at"]:
                setattr(obj, key, value)

        storage.save()
        return jsonify(obj.to_dict()), 200
