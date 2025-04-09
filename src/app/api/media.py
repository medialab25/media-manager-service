"""
Media management endpoints.
"""
import requests
from flask import Blueprint, jsonify
from ..core.config import settings

media_bp = Blueprint("media", __name__, url_prefix="/media-refresh")


@media_bp.route("", methods=["POST"])
def refresh_media():
    """Refresh media endpoint."""
    if not settings.jellyfin_api_key:
        return (
            jsonify({"status": "error", "message": "Jellyfin API key not configured"}),
            500,
        )

    headers = {
        "X-MediaBrowser-Token": settings.jellyfin_api_key,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            f"{settings.jellyfin_url}/Library/Refresh", headers=headers
        )
        response.raise_for_status()
        return (
            jsonify(
                {"status": "success", "message": "Jellyfin library refresh initiated"}
            ),
            200,
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500
