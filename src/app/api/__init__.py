"""
API package initialization.
"""
from .health import health_bp
from .media import media_bp

__all__ = ["health_bp", "media_bp"]
