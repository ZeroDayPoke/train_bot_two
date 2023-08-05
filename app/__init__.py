#!/usr/bin/env python
"""Initialize Flask app"""

# Fix for werkzeug bug
import werkzeug
werkzeug.secure_filename = werkzeug.utils.secure_filename
werkzeug.FileStorage = werkzeug.datastructures.FileStorage

from flask import Flask, render_template
from config import config
from flask_uploads import configure_uploads
from flask_login import LoginManager

from app.models import db, User
from app.routes import main_routes, auth_routes, admin_routes, project_routes

from app.utils.upload_sets import photos

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize Extensions
    login_manager = LoginManager()
    login_manager.init_app(app)
    db.init_app(app)
    configure_uploads(app, photos)

    # Register Blueprints
    blueprints = [main_routes, auth_routes, admin_routes, project_routes]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    app.url_map.strict_slashes = False

    @login_manager.user_loader
    def load_user(user_id):
        # Retrieve the user object based on the user_id
        user = User.query.get(user_id)
        return user

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        # Remove the database session after each request
        db.session.remove()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    if app.config.get('OPEN_BROWSER'):
        import webbrowser
        webbrowser.open('http://127.0.0.1:5000')

    return app

