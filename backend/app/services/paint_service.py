from app.db import connect
from app.engines.estimate import estimate_room
from app.repositories import openings, rooms, runs, settings

class PaintService:
    def __init__(self): self._c = connect()
    def close(self): self._c.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def list_rooms(self): return rooms.list_all(self._c)
    def room_detail(self, rid):
        r = rooms.get(self._c, rid)
        if not r: return None
        return {"room": r, "openings": openings.for_room(self._c, rid)}
    def settings(self): return settings.get_map(self._c)
    def history(self, limit=50): return runs.list_recent(self._c, limit)
    def estimate(self, room_id, persist, coats=None, coverage=None, band=None):
        detail = self.room_detail(room_id)
        if not detail: return None
        r = detail["room"]
        cov, ct = settings.coverage_coats(self._c)
        cov = float(coverage or cov)
        ct = int(coats or ct)
        ops = [{"w": o["w"], "h": o["h"]} for o in detail["openings"]]
        band_in = self._norm_band(band, ct)
        result = estimate_room(r["length"], r["width"], r["height"], ops, cov, ct, band_in)
        payload = {"room_id": room_id, "coats": ct, "coverage": cov}
        if band_in: payload["band"] = band_in
        rid = runs.insert(self._c, "estimate", payload, result, room_id) if persist else None
        return {"run_id": rid, "room_id": room_id, **result}
    @staticmethod
    def _norm_band(band, coats):
        if not band or not band.enabled: return None
        missing = [k for k in ("waist_height", "lower_coverage", "upper_coverage")
                   if getattr(band, k) is None]
        if missing: raise ValueError(f"band missing: {','.join(missing)}")
        return {"enabled": True,
                "waist_height": float(band.waist_height),
                "lower_coverage": float(band.lower_coverage),
                "upper_coverage": float(band.upper_coverage),
                "lower_coats": int(band.lower_coats or coats),
                "upper_coats": int(band.upper_coats or coats)}
    def dashboard(self):
        rs = rooms.list_all(self._c)
        return {"room_count": len(rs), "clean": len([x for x in rs if "种子" not in x["name"] and "多种" not in x["name"]]), "dirty": len([x for x in rs if "多种" in x["name"]])}
