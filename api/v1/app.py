#!/usr/bin/python3
"""Flask app"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exception):
    """Close database session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    POST = getenv('HBNB_API_PORT', 5000)
    app.run(debug=True, host=HOST, port=POST, threaded=True)
