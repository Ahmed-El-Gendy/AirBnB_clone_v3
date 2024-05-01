#!/usr/bin/python3
"""Index view"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Return status"""
    response = {"status": "OK"}
    return jsonify(response)

@app_views.route('/stats')
def get_stats():
    """Endpoint that retrieves the number of each objects by type"""
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    response = {}
    for key, value in classes.items():
        response[value] = storage.count(key)
    return jsonify(response)
