#!/usr/bin/python3
"""Comment here"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)


@app.teardown_appcontext
def teardown_appcontext(Exception):
    """close storage session"""
    storage.close()


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = int(getenv("HBNB_API_PORT"))
    app.run(host=host, port=port, threaded=True)