#!/usr/bin/python3
"""States View"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def allstates():
    """Retrieve list of all state objects"""
    return jsonify([s.to_dict() for s in storage.all("State").values()])


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createstate():
    """Creates a state"""
    data = ""
    try:
        data = request.get_json()
    except:
        abort("Not a JSON", 400)
    if not data.get('name'):
        abort("Missing name", 400)
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state(state_id=""):
    """State by id get, delete, and put"""
    for state in storage.all("State").values():
        if state.id == state_id:
            meth = request.method
            if meth == 'GET':
                return jsonify(state.to_dict())
            if meth == 'DELETE':
                state.delete()
                storage.save()
                return jsonify({}), 200
            if meth == 'PUT':
                data = ""
                try:
                    data = request.get_json()
                except:
                    abort("Not a JSON", 400)
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(state, k, v)
                state.save()
                return jsonify(state.to_dict()), 200
    abort(404)
