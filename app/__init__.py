import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dfdbd7e2-36d8-4dda-87d2-ea2171064eef'
    # SQLite database file placed in the persistent "data" folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data', 'rca.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Directory for custom files (logos, images, etc.) in persistent "custom_assets"
    app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'custom_assets')
    
    db.init_app(app)
    
    with app.app_context():
        from app import routes
        db.create_all()
    
    # Route to serve custom assets (e.g. background image)
    @app.route('/custom_assets/<path:filename>')
    def custom_assets(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

