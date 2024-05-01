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
