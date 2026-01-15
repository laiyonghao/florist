from __future__ import annotations

from typing import Any, Optional

from flask import Flask

from .generator import ensure_thumb


def _thumb_filter(
    src_url: Any, spec: str, *, alt: Optional[str] = None
) -> Any:
    if not src_url:
        return src_url

    try:
        url = str(src_url)
        out_url = ensure_thumb(url, spec)
        return out_url or url
    except Exception:
        # Contract: fail open.
        if alt is not None:
            return alt
        return src_url


def register_thumb_filter(app: Flask) -> None:
    # Expose as: {{ url|thumb('w200h200cc-q70jpg') }}
    app.add_template_filter(_thumb_filter, name="thumb")
