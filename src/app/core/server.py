"""
Flask server configuration and initialization.
"""
from flask import Flask
from .config import settings

app = Flask(__name__)
app.config.from_object(settings)

# Register blueprints
from ..api import health_bp
app.register_blueprint(health_bp)

def create_app() -> Flask:
    """Create and configure Flask application."""
    return app 