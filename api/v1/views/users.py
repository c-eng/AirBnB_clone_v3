#!/usr/bin/python3
"""Users View"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def allusers():
    """Retrieve list of all user objects"""
    return jsonify([u.to_dict() for u in storage.all("User").values()])


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createuser():
    """Creates a user"""
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400
    if not data.get('email'):
        return "Missing email", 400
    if not data.get('password'):
        return "Missing password", 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user(user_id=""):
    """User by id get, delete, and put"""
    for user in storage.all("User").values():
        if user.id == user_id:
            meth = request.method
            if meth == 'GET':
                return jsonify(user.to_dict())
            if meth == 'DELETE':
                user.delete()
                storage.save()
                return jsonify({}), 200
            if meth == 'PUT':
                data = request.get_json(silent=True)
                if not data:
                    return "Not a JSON", 400
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(user, k, v)
                user.save()
                return jsonify(user.to_dict()), 200
    abort(404)
