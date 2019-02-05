#!/usr/bin/python3
"""Routes for flask"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """/status response"""
    return jsonify(status="OK")
