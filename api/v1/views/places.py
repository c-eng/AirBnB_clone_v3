#!/usr/bin/python3
"""Places View"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def allplaces(city_id=""):
    """Retrieve list of all place objects by city"""
    if city_id:
        for c in storage.all("City").values():
            if c.id == city_id:
                return jsonify([p.to_dict() for p in c.places])
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def createplace(city_id=""):
    """Creates a place by city"""
    if city_id not in [c.id for c in storage.all("City").values()]:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400
    uid = data.get('user_id')
    if not uid:
        return "Missing user_id", 400
    if uid not in [u.id for u in storage.all("User").values()]:
        abort(404)
    if not data.get('name'):
        return "Missing name", 400
    data['city_id'] = city_id
    p = Place(**data)
    p.save()
    return jsonify(p.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place(place_id=""):
    """place by id get, delete, and put"""
    for p in storage.all("Place").values():
        if p.id == place_id:
            meth = request.method
            if meth == 'GET':
                return jsonify(p.to_dict())
            if meth == 'DELETE':
                p.delete()
                storage.save()
                return jsonify({}), 200
            if meth == 'PUT':
                data = request.get_json(silent=True)
                if not data:
                    return "Not a JSON", 400
                for k, v in data.items():
                    if k not in ['id', 'user_id', 'city_id',
                                 'created_at', 'updated_at']:
                        setattr(p, k, v)
                p.save()
                return jsonify(p.to_dict()), 200
    abort(404)
