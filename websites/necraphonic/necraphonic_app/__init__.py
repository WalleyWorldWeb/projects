# necraphonic_app/__init__.py
# --- Imports ---
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # For handling DB schema changes
import os
from dotenv import load_dotenv

# --- Database and Migration Initialization ---
# Initialize extensions here, outside the factory function
db = SQLAlchemy()
migrate = Migrate()

# --- Application Factory Function ---
def create_app():
    """Creates and configures the Flask application instance."""

    # --- Create Flask App Instance ---
    # Use instance_relative_config=True to load config files from 'instance' folder if they exist
    app = Flask(__name__, instance_relative_config=True)

    # --- Load Environment Variables ---
    # Construct the path to the .env file in the parent directory of the app package
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(app.instance_path)), '.env')
    load_dotenv(dotenv_path=dotenv_path)
    # Alternatively, if .env is in the project root (same level as app.py):
    # load_dotenv(os.path.join(os.path.dirname(app.root_path), '.env'))

    # --- Configuration ---
    # Load default configuration from config.py
    app.config.from_object('config.Config')
    # Load instance configuration if it exists (e.g., instance/config.py) - optional
    # app.config.from_pyfile('config.py', silent=True)

    # Ensure the instance folder exists (for SQLite DB, instance config, etc.)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # Directory already exists
        pass

    # --- Database Configuration ---
    # Set the database URI, prioritizing DATABASE_URL from .env,
    # otherwise use SQLite in the instance folder.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(app.instance_path, 'necraphonic.db')
    # Disable modification tracking for SQLAlchemy to save resources
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Explicitly set if not in config.Config

    # --- Initialize Flask Extensions with the App ---
    db.init_app(app)
    migrate.init_app(app, db) # Initialize Flask-Migrate

    # --- Import and Register Blueprints ---
    # Import blueprints *inside* the factory function to avoid circular imports
    from .routes.main import main_bp
    from .routes.music import music_bp
    from .routes.shows import shows_bp
    # Import contact blueprint when ready
    # from .routes.contact import contact_bp

    # Register blueprints with the app instance
    app.register_blueprint(main_bp) # No URL prefix for main routes usually
    app.register_blueprint(music_bp, url_prefix='/music')
    app.register_blueprint(shows_bp, url_prefix='/shows')
    # Register contact blueprint when ready
    # app.register_blueprint(contact_bp, url_prefix='/contact')

    # --- Import Database Models ---
    # Import models *after* initializing db and within the app context scope
    # This ensures models are registered with SQLAlchemy correctly, especially for Flask-Migrate
    with app.app_context():
        from . import models # Import models to make them known to SQLAlchemy/Migrate

    # --- Optional: Context Processors or CLI Commands ---
    # Example: Inject current year into templates
    # @app.context_processor
    # def inject_current_year():
    #     from datetime import datetime
    #     return {'current_year': datetime.utcnow().year}

    # --- Return the Configured App Instance ---
    return app
