#!/usr/bin/python3
"""Route for the State objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request
import json
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def amenities():
    list_amenities = []
    object_amenities = storage.all(Amenity)
    print(object_amenities)
    if object_amenities is None:
        abort(404)
    for key, value in object_amenities.items():
        list_amenities.append(value.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<id>', strict_slashes=False)
def get_amenity_by_id(id):
    """retrive an amenity by id"""
    obj = storage.get(Amenity, id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/amenities/<id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(id):
    """delete a state by id"""
    obj = storage.get(Amenity, id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """Returns the new City with the status code 201"""
    data = request.get_json()

    if data is None:
        return "Not a JSON\n", 400
    elif "name" not in data:
        return "Missing name\n", 400
    else:
        """Create a new City object"""
        obj = Amenity()
        obj.name = data["name"]
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<id>", methods=["PUT"], strict_slashes=False)
def put_amenity(id):
    """PUT method with the id"""

    obj = storage.get(Amenity, id)

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
