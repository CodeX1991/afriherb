#!/usr/bin/python3
"""Flask App module"""

# Imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """Initialize a flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'holiz_15'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth


    # Register the blueprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    # Create the database if it does not exist
    with app.app_context():
        db.create_all()

    # Return the app to where it is called
    return app
