#!/usr/bin/python3
"""routes of index page"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """return the status of the API"""
    return jsonify(status="OK")
