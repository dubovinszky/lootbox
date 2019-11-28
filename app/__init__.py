import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize application
app = Flask(__name__, static_folder=None)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)


# Initialize Flask Sql Alchemy
db = SQLAlchemy(app)

from app.views.api import api_bp  # noqa
app.register_blueprint(api_bp)

from app.views.app import app_bp  # noqa
app.register_blueprint(app_bp)
