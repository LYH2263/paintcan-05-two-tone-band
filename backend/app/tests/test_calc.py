import pytest
from app.engines.estimate import estimate_room
from app.engines.paint_volume import paint_liters
from app.engines.wall_area import wall_area
from app.modules.two_tone_band import BandError, split_net

OPS = [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}]

def test_living_room_net():
    a = wall_area(5, 4, 2.8, OPS)
    assert a["gross_m2"] == 50.4
    assert a["net_m2"] == 46.41

def test_liters_two_coats():
    v = paint_liters(46.41, 8, 2)
    assert v["liters"] == 11.6

def test_estimate_combined():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2)
    assert e["liters"] == 11.6

def test_bad_coverage():
    with pytest.raises(ValueError):
        paint_liters(10, 0, 2)

def test_band_off_matches_legacy():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2)
    assert e["band"] is False
    assert e["net_m2"] == 46.41
    assert e["liters"] == 11.6

def test_split_net_ratio():
    lower, upper = split_net(46.41, 2.8, 1.0)
    assert lower == pytest.approx(16.575)
    assert upper == pytest.approx(29.835)

def test_band_on_splits_and_totals():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2, band=True, waist_height=1.0,
                      lower_coverage=6, lower_coats=3, upper_coverage=10, upper_coats=1)
    assert e["band"] is True
    assert e["waist_height"] == 1.0
    # 开洞只扣一次：净面积不变，两带面积加回净面积
    assert e["net_m2"] == 46.41
    assert e["lower_band"]["net_m2"] + e["upper_band"]["net_m2"] == pytest.approx(46.41)
    assert e["lower_band"]["liters"] == round(e["lower_band"]["net_m2"] * 3 / 6, 2)
    assert e["upper_band"]["liters"] == round(e["upper_band"]["net_m2"] * 1 / 10, 2)
    assert e["liters"] == round(e["lower_band"]["liters"] + e["upper_band"]["liters"], 2)

def test_band_rejects_bad_waist():
    for bad in (0, -0.5, 2.8, 3.5, None):
        with pytest.raises((BandError, ValueError)):
            estimate_room(5, 4, 2.8, OPS, 8, 2, band=True, waist_height=bad,
                          lower_coverage=8, lower_coats=2, upper_coverage=8, upper_coats=2)

def test_band_rejects_nonpositive_coverage():
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, OPS, 8, 2, band=True, waist_height=1.0,
                      lower_coverage=0, lower_coats=2, upper_coverage=8, upper_coats=2)
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, OPS, 8, 2, band=True, waist_height=1.0,
                      lower_coverage=8, lower_coats=2, upper_coverage=-1, upper_coats=2)

def test_band_rejects_nonpositive_coats():
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, OPS, 8, 2, band=True, waist_height=1.0,
                      lower_coverage=8, lower_coats=0, upper_coverage=8, upper_coats=2)
