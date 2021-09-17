from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():

    app = Flask(__name__)
    CORS(app)
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=365)

    jwt = JWTManager(app)

    from .views import main
    app.register_blueprint(main)
    return app
