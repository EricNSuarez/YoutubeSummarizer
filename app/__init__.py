from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize components
    from app.routes import main
    app.register_blueprint(main)
    app.secret_key = app.config['SECRET_KEY']

    return app