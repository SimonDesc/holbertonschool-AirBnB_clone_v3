#!/usr/bin/python3
"""register blueprint and basics rule of flask app"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify
from flask_cors import CORS

"""create an instance of Flask"""
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

"""register a blueprint"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(err):
    """method called when the instance is at the end"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """method to return a 404 error"""
    return jsonify(error="Not found"), 404


"""define with the ENV the port and host"""
if __name__ == "__main__":
    host_hbnb = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port_hbnb = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host_hbnb, port=port_hbnb, threaded=True)
