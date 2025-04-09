"""
Merge operations endpoints.
"""

from flask import Blueprint, jsonify, request

merge_bp = Blueprint("merge", __name__)


@merge_bp.route("/merge-folders", methods=["POST"])
def merge_folders():
    """Merge folders endpoint."""
    # TODO: Implement folder merging logic
    return jsonify({"status": "success", "message": "Folder merge initiated"}), 200
