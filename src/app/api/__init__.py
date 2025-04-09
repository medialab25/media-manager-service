"""
API package initialization.
"""
from .health import health_bp
from .media import media_bp
from .merge import merge_bp

__all__ = ["health_bp", "media_bp", "merge_bp"]
