"""墙腰双色分带: split net wall area at the waistline into lower/upper bands.

Openings are deducted exactly once upstream (engines.wall_area); this module
only splits the resulting net area by band-height ratio — openings are never
re-deducted per band. Each band converts to liters with its own coverage and
coats. Invalid waist height or non-positive band coverage raises ValueError
so the caller rejects the whole request without persisting anything.
"""
from app.engines.paint_volume import paint_liters


def validate_waist(height: float, waist_height: float) -> float:
    h = float(height)
    w = float(waist_height)
    if w <= 0 or w >= h:
        raise ValueError("waist_height must be > 0 and < room height")
    return w


def split_net(net_m2: float, height: float, waist_height: float) -> tuple[float, float]:
    """Split net area into (lower, upper) by band-height ratio; sums to net_m2."""
    w = validate_waist(height, waist_height)
    lower = round(float(net_m2) * w / float(height), 2)
    upper = round(float(net_m2) - lower, 2)
    return lower, upper


def band_liters(net_m2: float, height: float, waist_height: float,
                lower_coverage: float, upper_coverage: float,
                lower_coats: int, upper_coats: int) -> dict:
    """Per-band liters plus total for a waist-split wall. Raises ValueError on
    bad waist height, non-positive coverage, or non-positive coats."""
    h = float(height)
    w = validate_waist(h, waist_height)
    lc, uc = float(lower_coverage), float(upper_coverage)
    if lc <= 0 or uc <= 0:
        raise ValueError("band coverage must be positive")
    lower_m2, upper_m2 = split_net(net_m2, h, w)
    low = paint_liters(lower_m2, lc, lower_coats)
    up = paint_liters(upper_m2, uc, upper_coats)
    return {
        "enabled": True,
        "waist_height": w,
        "lower": {"height_m": round(w, 2), "net_m2": lower_m2, "coverage": lc,
                  "coats": int(lower_coats), "liters": low["liters"]},
        "upper": {"height_m": round(h - w, 2), "net_m2": upper_m2, "coverage": uc,
                  "coats": int(upper_coats), "liters": up["liters"]},
        "total_liters": round(low["liters"] + up["liters"], 2),
    }
