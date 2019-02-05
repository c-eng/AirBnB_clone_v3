#!/usr/bin/python3
"""Blueprint for Flask?"""
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
if app_views:
    from api.v1.views.index import *
    from api.v1.views import states, cities, amenities, users, places
