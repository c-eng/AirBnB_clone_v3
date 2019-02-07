#!/usr/bin/python3
"""Blueprint for Flask?"""
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *  # noqa
from api.v1.views import states  # noqa
from api.v1.views import cities  # noqa
from api.v1.views import amenities  # noqa
from api.v1.views import users  # noqa
from api.v1.views import places  # noqa
from api.v1.views import places_reviews  # noqa
from api.v1.views import places_amenities  # noqa
