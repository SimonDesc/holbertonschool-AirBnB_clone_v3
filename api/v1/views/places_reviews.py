#!/usr/bin/python3
"""Places reviews objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review_by_place_id(place_id):
    """Retrieves the list of all Review objects of a Place"""
    obj_review = storage.get(Place, place_id)
    if obj_review is None:
        abort(404)

    """Get the list of reviews associated with the Place object"""
    all_reviews_list = obj_review.reviews

    review_list = []
    """Convert each review to a dictionary"""
    for place in all_reviews_list:
        review_list.append(place.to_dict())

    return jsonify(review_list), 200


@app_views.route('reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review_id(review_id):
    """Retrieves a Review object bu his id"""
    obj_review_id = storage.get(Review, review_id)
    if obj_review_id is None:
        abort(404)
    return jsonify(obj_review_id.to_dict())


@app_views.route('reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def review_delete(review_id):
    """Delete a Review object bu his id"""
    empty = {}
    obj_review_id = storage.get(Review, review_id)
    if obj_review_id is None:
        abort(404)
    storage.delete(obj_review_id)
    storage.save()
    return (jsonify(empty), 200)


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def review_create(place_id):
    """Returns the new Review with the status code 201"""
    data = request.get_json()

    obj_review = storage.get(Place, place_id)
    if obj_review is None:
        abort(404)

    if data is None:
        return "Not a JSON\n", 400
    if "user_id" not in data:
        return "Missing user_id\n", 400

    """Check if the user exists"""
    user_id = data['user_id']
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    """Check if 'text' is present in the data"""
    if 'text' not in data:
        return "Missing text\n", 400

    """Create a new Place object"""
    obj_review = Review()
    obj_review.text = data["text"]
    obj_review.place_id = place_id
    obj_review.user_id = user_id
    storage.new(obj_review)
    storage.save()
    return jsonify(obj_review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_update(review_id):
    """Update a Review object by his id"""
    obj_update = storage.get(Review, review_id)
    if obj_update is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON\n", 400
        else:
            for key, value in data.items():
                if key not in ["id", "user_id", "place_id",
                               "created_at", "updated_at"]:
                    setattr(obj_update, key, value)
            storage.save()

        return jsonify(obj_update.to_dict()), 200
