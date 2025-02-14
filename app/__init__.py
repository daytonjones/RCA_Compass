# app/__init__.py
from flask import Flask
from app.models import db, init_db

def create_app():
    app = Flask(__name__)
    # You may want to set a strong secret key in real usage
    app.config['SECRET_KEY'] = 'f5a3e0c1-a7d3-4e97-8036-a79efe7687ab'
    # Configure the path for SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rca_compass.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        init_db()

    return app

