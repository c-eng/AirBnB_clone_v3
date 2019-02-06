#!/usr/bin/python3
"""Amenities View"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def allamenities():
    """Retrieve list of all amenity objects"""
    return jsonify([a.to_dict() for a in storage.all("Amenity").values()])


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createamenity():
    """Creates an amenity"""
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400
    if not data.get('name'):
        return "Missing name", 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity(amenity_id=""):
    """Amenity by id get, delete, and put"""
    for a in storage.all("Amenity").values():
        if a.id == amenity_id:
            meth = request.method
            if meth == 'GET':
                return jsonify(a.to_dict())
            if meth == 'DELETE':
                a.delete()
                storage.save()
                return jsonify({}), 200
            if meth == 'PUT':
                data = request.get_json(silent=True)
                if not data:
                    return "Not a JSON", 400
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(a, k, v)
                a.save()
                return jsonify(a.to_dict()), 200
    abort(404)
