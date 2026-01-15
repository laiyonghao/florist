from __future__ import annotations

import hashlib
import os
import pathlib
import tempfile
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse

from flask import current_app

from .spec import ThumbSpecError, split_spec
from .transform import transform_image


@dataclass(frozen=True)
class ResolvedSource:
    src_url: str
    url_path: str
    fs_path: pathlib.Path
    rel_key: str  # stable identifier for cache keys


def _get_uploaded_path() -> pathlib.Path:
    p = current_app.config.get("UPLOADED_PATH")
    if not p:
        raise RuntimeError("UPLOADED_PATH is not configured")
    return pathlib.Path(p)


def _get_cache_dir() -> pathlib.Path:
    cache_dir = current_app.config.get("THUMBS_CACHE_DIR")
    if cache_dir:
        return pathlib.Path(cache_dir)

    subdir = current_app.config.get("THUMBS_CACHE_SUBDIR", "_thumbs")
    return _get_uploaded_path() / subdir


def _allowed_formats() -> Tuple[str, ...]:
    allowed = current_app.config.get("THUMBS_ALLOWED_FORMATS")
    if not allowed:
        return ("jpg", "png", "webp")
    return tuple([str(x).lower().strip(".") for x in allowed])


def _resolve_source(url: str) -> Optional[ResolvedSource]:
    parsed = urlparse(url)
    url_path = parsed.path or ""

    prefixes: Dict[str, str] = (
        current_app.config.get("THUMBS_SOURCE_PREFIXES") or {}
    )
    if not prefixes:
        return None

    uploaded_root = _get_uploaded_path()

    for url_prefix, fs_subdir in prefixes.items():
        if not url_prefix:
            continue
        if not url_prefix.startswith("/"):
            url_prefix = "/" + url_prefix
        if not url_prefix.endswith("/"):
            url_prefix = url_prefix + "/"

        if not url_path.startswith(url_prefix):
            continue

        suffix = url_path[len(url_prefix):]
        # Avoid path traversal.
        if ".." in suffix.split("/"):
            return None

        fs_base = pathlib.Path(fs_subdir)
        if not fs_base.is_absolute():
            fs_base = uploaded_root / fs_base

        fs_path = (fs_base / suffix).resolve()
        try:
            fs_base_resolved = fs_base.resolve()
        except Exception:
            fs_base_resolved = fs_base

        # Ensure fs_path is under base.
        if fs_base_resolved not in fs_path.parents and (
            fs_path != fs_base_resolved
        ):
            return None

        rel_key = f"{url_prefix}|{suffix}"
        return ResolvedSource(
            src_url=url,
            url_path=url_path,
            fs_path=fs_path,
            rel_key=rel_key,
        )

    return None


def _source_fingerprint(path: pathlib.Path) -> str:
    st = path.stat()
    # Good-enough invalidation: mtime+size.
    return f"{st.st_size}:{st.st_mtime_ns}"


def _build_output_path(
    cache_dir: pathlib.Path, key: str, ext: str
) -> Tuple[pathlib.Path, str]:
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()
    d1, d2 = h[:2], h[2:4]
    rel = f"{d1}/{d2}/{h}.{ext}"
    return cache_dir / rel, rel


def ensure_thumb(src_url: str, raw_spec: str) -> Optional[str]:
    if not current_app.config.get("THUMBS_ENABLED", True):
        return None

    resolved = _resolve_source(src_url)
    if not resolved:
        return None

    if not resolved.fs_path.exists():
        return None

    try:
        spec, spec_key = split_spec(raw_spec)
    except ThumbSpecError:
        return None

    allowed = _allowed_formats()

    src_ext = resolved.fs_path.suffix.lower().lstrip(".")
    if src_ext == "jpeg":
        src_ext = "jpg"

    out_fmt = (spec.fmt or src_ext or "jpg").lower().strip(".")
    if out_fmt == "jpeg":
        out_fmt = "jpg"

    if out_fmt not in allowed:
        return None

    quality_default = int(current_app.config.get("THUMBS_DEFAULT_QUALITY", 70))
    quality = spec.quality
    if quality is None and out_fmt in ("jpg", "webp"):
        quality = quality_default

    cache_dir = _get_cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)

    fp = _source_fingerprint(resolved.fs_path)
    cache_key = f"{resolved.rel_key}|{fp}|{spec_key}|{out_fmt}|q{quality}"

    out_path, rel = _build_output_path(cache_dir, cache_key, out_fmt)
    url_prefix = str(
        current_app.config.get("THUMBS_URL_PREFIX", "/thumbs")
    ).rstrip("/")

    if out_path.exists():
        return f"{url_prefix}/{rel}"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Best-effort: allow duplicate concurrent generation.
    tmp_fd = None
    tmp_path = None
    try:
        tmp_fd, tmp_path = tempfile.mkstemp(
            prefix=".tmp-", dir=str(out_path.parent)
        )
        os.close(tmp_fd)
        transform_image(
            src_path=resolved.fs_path,
            dst_path=pathlib.Path(tmp_path),
            spec=spec,
            out_fmt=out_fmt,
            quality=quality,
        )
        os.replace(tmp_path, out_path)
    finally:
        try:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except Exception:
            pass

    return f"{url_prefix}/{rel}"
