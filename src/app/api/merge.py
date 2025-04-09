"""
Merge operations endpoints.
"""

from flask import Blueprint, jsonify, request
from ..core.merge import FolderMerger
from ..core.config import settings

merge_bp = Blueprint("merge", __name__)


@merge_bp.route("/merge-folders", methods=["POST"])
def merge_folders():
    """Merge folders endpoint."""
    try:
        merger = FolderMerger(
            settings.merge["input_folders"], settings.merge["output_folder"]
        )
        merger.merge()
        return (
            jsonify({"status": "success", "message": "Folders merged successfully"}),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
