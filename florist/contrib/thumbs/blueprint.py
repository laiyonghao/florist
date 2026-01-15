from __future__ import annotations

import pathlib

from flask import Blueprint, abort, current_app, send_from_directory


thumbs_bp = Blueprint("thumbs", __name__)


@thumbs_bp.route("/<path:filename>")
def serve_thumb(filename: str):
    cache_dir_cfg = current_app.config.get("THUMBS_CACHE_DIR")
    if cache_dir_cfg:
        cache_dir = pathlib.Path(cache_dir_cfg)
    else:
        uploaded = current_app.config.get("UPLOADED_PATH")
        if not uploaded:
            abort(404)
        subdir = current_app.config.get("THUMBS_CACHE_SUBDIR", "_thumbs")
        cache_dir = pathlib.Path(uploaded) / subdir

    response = send_from_directory(cache_dir, filename)
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return response
