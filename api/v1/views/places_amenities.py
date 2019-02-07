#!/usr/bin/python3
"""Place_Amenity View"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def place_amenities(place_id="", amenity_id=""):
    """Operations on place_amenities routes"""
    place_list = [p for p in storage.all("Place").values()]
    if place_id not in [p.id for p in place_list]:
        abort(404)
    if request.method == "GET" and not amenity_id:
        for p in place_list:
            if p.id == place_id:
                return jsonify([a.to_dict() for a in p.amenities])
        abort(404)
    amenity_list = [a for a in storage.all("Amenity").values()]
    if amenity_id not in [a.id for a in amenity_list]:
        abort(404)
    p = storage.get("Place", place_id)
    a = storage.get("Amenity", amenity_id)
    if request.method == "DELETE":
        if a in p.amenities:
            p.amenities.remove(a)
            p.save()
            return jsonify({}), 200
        abort(404)
    if request.method == "POST":
        if a in p.amenities:
            return jsonify(a.to_dict()), 200
        p.amenities.append(a)
        p.save()
        return jsonify(a.to_dict()), 201
