#!/usr/bin/python3
"""Reviews View"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def allreviews(place_id=""):
    """Retrieve list of all review objects by place"""
    if place_id:
        for p in storage.all("Place").values():
            if p.id == place_id:
                return jsonify([r.to_dict() for r in p.reviews])
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def createreview(place_id=""):
    """Creates a review by place"""
    if place_id not in [p.id for p in storage.all("Place").values()]:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400
    uid = data.get('user_id')
    if not uid:
        return "Missing user_id", 400
    if uid not in [u.id for u in storage.all("User").values()]:
        abort(404)
    if not data.get('text'):
        return "Missing text", 400
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review(review_id=""):
    """Review by id get, delete, and put"""
    for r in storage.all("Review").values():
        if r.id == review_id:
            meth = request.method
            if meth == 'GET':
                return jsonify(r.to_dict())
            if meth == 'DELETE':
                r.delete()
                storage.save()
                return jsonify({}), 200
            if meth == 'PUT':
                data = request.get_json(silent=True)
                if not data:
                    return "Not a JSON", 400
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at', 'user_id',
                                 'place_id']:
                        setattr(r, k, v)
                r.save()
                return jsonify(r.to_dict()), 200
    abort(404)
