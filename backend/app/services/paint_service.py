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

    def estimate(self, room_id, persist, coats=None, coverage=None,
                 band=False, waist_height=None,
                 lower_coverage=None, lower_coats=None,
                 upper_coverage=None, upper_coats=None):
        detail = self.room_detail(room_id)
        if not detail: return None
        r = detail["room"]
        cov, ct = settings.coverage_coats(self._c)
        cov = float(coverage or cov)
        ct = int(coats or ct)
        ops = [{"w": o["w"], "h": o["h"]} for o in detail["openings"]]

        lower_cov = float(lower_coverage if lower_coverage is not None else cov)
        lower_ct = int(lower_coats if lower_coats is not None else ct)
        upper_cov = float(upper_coverage if upper_coverage is not None else cov)
        upper_ct = int(upper_coats if upper_coats is not None else ct)

        # 先算后写：任何非法入参在此抛出，整单拒绝且不落记录
        result = estimate_room(
            r["length"], r["width"], r["height"], ops, cov, ct,
            band=band, waist_height=waist_height,
            lower_coverage=lower_cov, lower_coats=lower_ct,
            upper_coverage=upper_cov, upper_coats=upper_ct,
        )

        if band:
            payload = {
                "room_id": room_id,
                "band": True,
                "waist_height": result["waist_height"],
                "lower_band": {"coverage": lower_cov, "coats": lower_ct},
                "upper_band": {"coverage": upper_cov, "coats": upper_ct},
            }
        else:
            payload = {"room_id": room_id, "coats": ct, "coverage": cov, "band": False}

        rid = runs.insert(self._c, "estimate", payload, result, room_id) if persist else None
        return {"run_id": rid, "room_id": room_id, **result}

    def dashboard(self):
        rs = rooms.list_all(self._c)
        return {"room_count": len(rs), "clean": len([x for x in rs if "种子" not in x["name"] and "多种" not in x["name"]]), "dirty": len([x for x in rs if "多种" in x["name"]])}
