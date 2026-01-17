"""
VybeFlow - Social Media Platform for Urban Artists
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    try:
        from .config import config
    except ImportError:
        from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints from available modules; fall back gracefully if optional ones are missing
    from .main import main_bp
    app.register_blueprint(main_bp)

    try:
        from .routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
    except ImportError:
        app.logger.warning("auth blueprint not found; authentication routes are disabled")

    try:
        from .routes.messaging import messaging_bp
        app.register_blueprint(messaging_bp, url_prefix='/messaging')
    except ImportError:
        app.logger.warning("messaging blueprint not found; messaging routes are disabled")
    
    return app