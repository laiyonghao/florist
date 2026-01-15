import re
from dataclasses import dataclass
from typing import Optional, Tuple


_MODE_RE = re.compile(r"(cc|c|s)$")


@dataclass(frozen=True)
class ThumbSpec:
    # Geometry
    width: Optional[int] = None
    height: Optional[int] = None
    scale_thousand: Optional[int] = None  # 1000 == 1.0
    mode: Optional[str] = None  # 'c' | 'cc' | 's' | None

    # Storage
    quality: Optional[int] = None  # 0..100
    fmt: Optional[str] = None  # 'jpg'|'png'|'webp'|...


class ThumbSpecError(ValueError):
    pass


def parse_thumb_spec(spec: str) -> ThumbSpec:
    """Parse DSL like:

    - w200h100cc-q70jpg
    - h100-q70jpg
    - s500-q85jpg  (scale = 0.5)
    - -q70jpg      (no geometry, only re-encode)

    Notes:
    - Uses '-' to split geometry and storage sections.
    - 'sNNN' is thousandth scaling ratio.
    - Mode suffix belongs to geometry section:
      'c' contain, 'cc' cover+crop, 's' stretch.
    """

    raw = (spec or "").strip()
    if not raw:
        raise ThumbSpecError("empty spec")

    if "-" in raw:
        geom_part, store_part = raw.split("-", 1)
    else:
        geom_part, store_part = raw, ""

    geom_part = geom_part.strip()
    store_part = store_part.strip()

    width: Optional[int] = None
    height: Optional[int] = None
    scale_thousand: Optional[int] = None
    mode: Optional[str] = None

    if geom_part:
        # mode suffix
        m = _MODE_RE.search(geom_part)
        if m:
            mode = m.group(1)
            geom_body = geom_part[: -len(mode)]
        else:
            geom_body = geom_part

        geom_body = geom_body.strip()
        if not geom_body:
            raise ThumbSpecError("invalid geometry")

        if geom_body.startswith("s"):
            if ("w" in geom_body) or ("h" in geom_body):
                raise ThumbSpecError("scale cannot be combined with w/h")
            if not re.fullmatch(r"s\d+", geom_body):
                raise ThumbSpecError("bad scale format")
            scale_thousand = int(geom_body[1:])
            if scale_thousand <= 0:
                raise ThumbSpecError("scale must be > 0")
            if mode:
                # Scale implies proportional resize;
                # explicit mode doesn't apply.
                raise ThumbSpecError("scale cannot have mode suffix")
        else:
            # parse w/h in any order
            tokens = re.findall(r"[wh]\d+", geom_body)
            if not tokens:
                raise ThumbSpecError("bad geometry format")
            rest = re.sub(r"[wh]\d+", "", geom_body)
            if rest.strip():
                raise ThumbSpecError("unknown geometry tokens")
            for t in tokens:
                if t.startswith("w"):
                    width = int(t[1:])
                elif t.startswith("h"):
                    height = int(t[1:])

            if (width is not None and width <= 0) or (
                height is not None and height <= 0
            ):
                raise ThumbSpecError("w/h must be > 0")

    quality: Optional[int] = None
    fmt: Optional[str] = None

    if store_part:
        # q is optional prefix
        if store_part.startswith("q"):
            m = re.match(r"q(\d{1,3})(.*)$", store_part)
            if not m:
                raise ThumbSpecError("bad quality format")
            quality = int(m.group(1))
            if quality < 0 or quality > 100:
                raise ThumbSpecError("quality must be 0..100")
            fmt = (m.group(2) or "").strip() or None
        else:
            fmt = store_part

        if fmt:
            fmt = fmt.lower().strip(".")

    return ThumbSpec(
        width=width,
        height=height,
        scale_thousand=scale_thousand,
        mode=mode,
        quality=quality,
        fmt=fmt,
    )


def canonicalize_spec(spec: ThumbSpec) -> ThumbSpec:
    """Normalize defaults; does not decide no-op vs not.

    - quality defaults are applied later
      (since format affects whether q is meaningful).
    - geometry mode defaults are applied here.
    """

    mode = spec.mode

    # Default mode rules
    if spec.scale_thousand is not None:
        mode = None
    elif spec.width is None or spec.height is None:
        # Single-edge resize implies contain
        mode = mode or "c"
    else:
        # Both w+h implies cover+crop
        mode = mode or "cc"

    fmt = spec.fmt.lower() if spec.fmt else None

    # Normalize jpeg extension
    if fmt == "jpeg":
        fmt = "jpg"

    return ThumbSpec(
        width=spec.width,
        height=spec.height,
        scale_thousand=spec.scale_thousand,
        mode=mode,
        quality=spec.quality,
        fmt=fmt,
    )


def spec_to_string(spec: ThumbSpec) -> str:
    """String form used for cache keys (canonical)."""

    geom = ""
    if spec.scale_thousand is not None:
        geom = f"s{spec.scale_thousand}"
    else:
        if spec.width is not None:
            geom += f"w{spec.width}"
        if spec.height is not None:
            geom += f"h{spec.height}"
        if geom and spec.mode:
            geom += spec.mode

    store = ""
    if spec.quality is not None:
        store += f"q{spec.quality}"
    if spec.fmt:
        store += spec.fmt

    if geom and store:
        return f"{geom}-{store}"
    if geom:
        return geom
    if store:
        return f"-{store}"
    return ""  # should not happen for valid specs


def split_spec(raw: str) -> Tuple[ThumbSpec, str]:
    parsed = parse_thumb_spec(raw)
    canon = canonicalize_spec(parsed)
    canon_str = spec_to_string(canon)
    return canon, canon_str
