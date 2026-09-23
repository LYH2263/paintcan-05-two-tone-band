import json
import pytest
from app import seed
from app.schemas.estimate import BandRequest
from app.services.paint_service import PaintService

BAND = {"waist_height": 1.12, "lower_coverage": 6, "upper_coverage": 9}

@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setattr("app.db.DB_PATH", tmp_path / "t.db")
    seed.init_db()

def band(**kw):
    return BandRequest(enabled=True, **{**BAND, **kw})

def history_count():
    with PaintService() as s:
        return len(s.history())

def test_band_off_matches_base():
    with PaintService() as s:
        r = s.estimate(1, False)
    assert r["liters"] == 11.6 and "band" not in r

def test_band_result_split_and_total():
    with PaintService() as s:
        r = s.estimate(1, False, band=band())
    assert r["run_id"] is None
    assert r["band"]["lower"]["liters"] == 6.19
    assert r["band"]["upper"]["liters"] == 6.19
    assert r["band"]["total_liters"] == 12.38

def test_persist_false_writes_nothing():
    before = history_count()
    with PaintService() as s:
        r = s.estimate(1, False, band=band())
    assert r["run_id"] is None
    assert history_count() == before

@pytest.mark.parametrize("kw", [{"waist_height": 0}, {"waist_height": 2.8},
                                {"lower_coverage": 0}, {"upper_coverage": -1}])
def test_invalid_band_rejected_writes_nothing(kw):
    before = history_count()
    with PaintService() as s:
        with pytest.raises(ValueError):
            s.estimate(1, True, band=band(**kw))
    assert history_count() == before

def test_missing_band_fields_rejected():
    with PaintService() as s:
        with pytest.raises(ValueError):
            s.estimate(1, True, band=BandRequest(enabled=True, waist_height=1.12))

def test_persist_pins_band_and_stays_immutable():
    with PaintService() as s:
        r1 = s.estimate(1, True, band=band())
        s.estimate(1, True, band=band(upper_coverage=5))  # later change must not rewrite r1
        rows = {h["id"]: h for h in s.history()}
    rec = rows[r1["run_id"]]
    res = json.loads(rec["result_json"])
    inp = json.loads(rec["input_json"])
    assert inp["band"]["waist_height"] == 1.12
    assert inp["band"]["upper_coverage"] == 9
    assert res["band"]["upper"]["coverage"] == 9
    assert res["band"]["upper"]["liters"] == 6.19
    assert res["band"]["total_liters"] == 12.38
