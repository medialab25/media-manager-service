"""
Flask server configuration and initialization.
"""
from flask import Flask
from .config import settings
from ..api import health_bp, media_bp, merge_bp

app = Flask(__name__)
app.config.from_object(settings)

# Register blueprints
app.register_blueprint(health_bp)
app.register_blueprint(media_bp)
app.register_blueprint(merge_bp)


def run_server():
    """Run the Flask server with configured settings."""
    app.run(host=settings.host, port=settings.port, debug=settings.debug)


def create_app() -> Flask:
    """Create and configure Flask application."""
    return app
