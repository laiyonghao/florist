from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from flask import current_app, url_for
from wtforms import StringField

from .widgets import ImageInputWidget


# 需要解决 admin 地址动态化的问题
# REF: https://stackoverflow.com/questions/50531796/
# flask-admin-extra-js-and-url-for
class ImageInputWidgetExtraJs:
    """Descriptor for injecting Florist's image_input_widget.js into `extra_js`.

    - Prefer `url_for('florist_bp.image_input_widget_js')` (handles url_prefix)
    - Fall back to string concatenation using `FLORIST_ADMIN_URL`

    Supports `extra_js` so callers can include other JS files.
    """

    def __init__(self, extra_js: Iterable[str] | None = None) -> None:
        self._extra_js = list(extra_js) if extra_js else []

    def __get__(self, inst: Any, owner: type | None = None) -> list[str]:
        items: list[str] = []
        for s in self._extra_js:
            if s and s not in items:
                items.append(s)

        def _admin_prefix() -> str:
            prefix = '/admin'
            try:
                prefix = current_app.config.get('FLORIST_ADMIN_URL', '/admin')
            except RuntimeError:
                pass

            if not prefix.startswith('/'):
                prefix = '/' + prefix
            return prefix.rstrip('/')

        widget_js: str | None = None
        try:
            widget_js = url_for('florist_bp.image_input_widget_js')
        except Exception:
            prefix = _admin_prefix()
            widget_js = f'{prefix}/florist/static/js/image_input_widget.js'

        if widget_js and widget_js not in items:
            items.append(widget_js)
        return items


class ImageField(StringField):
    widget = ImageInputWidget()
