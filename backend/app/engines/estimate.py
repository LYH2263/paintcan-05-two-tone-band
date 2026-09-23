from app.engines.paint_volume import paint_liters
from app.engines.wall_area import wall_area
from app.modules import waist_band

def estimate_room(length, width, height, openings, coverage, coats, band=None):
    area = wall_area(length, width, height, openings)
    if not band or not band.get("enabled"):
        vol = paint_liters(area["net_m2"], coverage, coats)
        return {**area, **vol}
    b = waist_band.band_liters(area["net_m2"], height, band["waist_height"],
                               band["lower_coverage"], band["upper_coverage"],
                               band.get("lower_coats") or coats,
                               band.get("upper_coats") or coats)
    return {**area, "liters": b["total_liters"], "coats": int(coats),
            "coverage": float(coverage), "band": b}
