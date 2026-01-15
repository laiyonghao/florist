from __future__ import annotations

from flask import Flask

from .filter import register_thumb_filter
from .blueprint import thumbs_bp


def init(app: Flask) -> None:
    if not app.config.get("THUMBS_ENABLED", True):
        return

    register_thumb_filter(app)

    # Provide a simple Flask route for serving generated thumbs.
    # In production you can serve THUMBS_CACHE_DIR via nginx/CDN.
    url_prefix = app.config.get("THUMBS_URL_PREFIX", "/thumbs")
    app.register_blueprint(thumbs_bp, url_prefix=url_prefix)
