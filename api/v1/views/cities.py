#!/usr/bin/python3
"""Cities View"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def allcities(state_id=""):
    """Retrieve list of all city objects by state id"""
    if state_id:
        for s in storage.all("State").values():
            if s.id == state_id:
                return jsonify([c.to_dict() for c in s.cities])
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city(city_id=""):
    """Operate on a city object by id"""
    if city_id:
        for c in storage.all("City").values():
            if c.id == city_id:
                meth = request.method
                if meth == "GET":
                    return jsonify(c.to_dict())
                if meth == "DELETE":
                    c.delete()
                    storage.save()
                    return jsonify({}), 200
                if meth == "PUT":
                    data = request.get_json(silent=True)
                    if not data:
                        return "Not a JSON", 400
                    for k, v in data.items():
                        if k not in ['id', 'created_at', 'updated_at']:
                            setattr(c, k, v)
                    c.save()
                    return jsonify(c.to_dict()), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createcity(state_id=""):
    """Creates a city"""
    if state_id not in [s.id for s in storage.all("State").values()]:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400
    if not data.get('name'):
        return "Missing name", 400
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201
