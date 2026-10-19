from flask import Flask
from app.routes import registered_routes


def create_app():
    app = Flask(__name__)
    registered_routes(app)
    return app