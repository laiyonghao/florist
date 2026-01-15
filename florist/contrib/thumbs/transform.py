from __future__ import annotations

import math
import pathlib
from typing import Optional, Tuple

from PIL import Image, ImageOps

from .spec import ThumbSpec


def _pillow_format(fmt: str) -> str:
    fmt = (fmt or "").lower().strip(".")
    if fmt == "jpg":
        return "JPEG"
    return fmt.upper()


def _clamp_scale_up(
    w: int, h: int, orig_w: int, orig_h: int, max_scale: float
) -> Tuple[int, int]:
    if max_scale <= 0:
        return w, h

    max_w = max(1, int(orig_w * max_scale))
    max_h = max(1, int(orig_h * max_scale))

    if w <= max_w and h <= max_h:
        return w, h

    scale = min(max_w / max(w, 1), max_h / max(h, 1))
    w2 = max(1, int(w * scale))
    h2 = max(1, int(h * scale))
    return w2, h2


def _compute_target_size(
    img: Image.Image, spec: ThumbSpec
) -> Tuple[int, int, str]:
    ow, oh = img.size

    if spec.scale_thousand is not None:
        f = spec.scale_thousand / 1000.0
        tw = max(1, int(math.floor(ow * f)))
        th = max(1, int(math.floor(oh * f)))
        return tw, th, "c"

    # Default behavior for missing edges.
    if spec.width is not None and spec.height is not None:
        return spec.width, spec.height, (spec.mode or "cc")

    if spec.width is not None:
        th = max(1, int(round(oh * (spec.width / ow))))
        return spec.width, th, "c"

    if spec.height is not None:
        tw = max(1, int(round(ow * (spec.height / oh))))
        return tw, spec.height, "c"

    # No geometry => no resize.
    return ow, oh, "c"


def transform_image(
    *,
    src_path: pathlib.Path,
    dst_path: pathlib.Path,
    spec: ThumbSpec,
    out_fmt: str,
    quality: Optional[int],
) -> None:
    cfg = _current_app().config
    max_scale_up = float(cfg.get("FLORIST_THUMBS_MAX_SCALE_UP", 2.0))
    max_dim = int(cfg.get("FLORIST_THUMBS_MAX_DIMENSION", 8192))

    with Image.open(src_path) as img:
        img = ImageOps.exif_transpose(img)
        ow, oh = img.size

        tw, th, mode = _compute_target_size(img, spec)

        # Absolute limits to avoid abuse.
        tw = max(1, min(int(tw), max_dim))
        th = max(1, min(int(th), max_dim))

        tw, th = _clamp_scale_up(tw, th, ow, oh, max_scale_up)

        if (tw, th) != (ow, oh):
            if mode == "cc":
                img = ImageOps.fit(
                    img,
                    (tw, th),
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5),
                )
            elif mode == "s":
                img = img.resize((tw, th), resample=Image.Resampling.LANCZOS)
            else:
                # contain
                img.thumbnail((tw, th), resample=Image.Resampling.LANCZOS)

        save_kwargs = {}

        if out_fmt == "jpg":
            # Ensure no alpha.
            if img.mode in ("RGBA", "LA") or (
                img.mode == "P" and "transparency" in img.info
            ):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                rgba = img.convert("RGBA")
                bg.paste(rgba, mask=rgba.split()[-1])
                img = bg
            else:
                img = img.convert("RGB")

            save_kwargs["optimize"] = True
            if quality is not None:
                save_kwargs["quality"] = int(quality)
            save_kwargs["progressive"] = True

        elif out_fmt == "webp":
            if quality is not None:
                save_kwargs["quality"] = int(quality)
            save_kwargs["method"] = 6

        elif out_fmt == "png":
            save_kwargs["optimize"] = True

        img.save(dst_path, format=_pillow_format(out_fmt), **save_kwargs)


def _current_app():
    # Lazy import to avoid circulars and allow tool usage outside Flask.
    from flask import current_app as _ca

    return _ca
