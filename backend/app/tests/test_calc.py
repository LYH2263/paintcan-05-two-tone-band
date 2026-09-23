import pytest
from app.engines.estimate import estimate_room
from app.engines.paint_volume import paint_liters
from app.engines.wall_area import wall_area
from app.modules import waist_band

OPENINGS = [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}]

def test_living_room_net():
    a = wall_area(5, 4, 2.8, [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}])
    assert a["gross_m2"] == 50.4
    assert a["net_m2"] == 46.41

def test_liters_two_coats():
    v = paint_liters(46.41, 8, 2)
    assert v["liters"] == 11.6

def test_estimate_combined():
    e = estimate_room(5, 4, 2.8, [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}], 8, 2)
    assert e["liters"] == 11.6

def test_bad_coverage():
    with pytest.raises(ValueError):
        paint_liters(10, 0, 2)

def test_band_split_sums_to_net():
    low, up = waist_band.split_net(46.41, 2.8, 1.12)
    assert low == 18.56 and up == 27.85
    assert round(low + up, 2) == 46.41

def test_band_openings_deducted_once():
    e = estimate_room(5, 4, 2.8, OPENINGS, 8, 2,
                      {"enabled": True, "waist_height": 1.12,
                       "lower_coverage": 6, "upper_coverage": 9})
    assert e["net_m2"] == 46.41  # same net as unbanded: holes not re-deducted
    assert e["band"]["lower"]["net_m2"] + e["band"]["upper"]["net_m2"] == 46.41

def test_band_liters_and_total():
    e = estimate_room(5, 4, 2.8, OPENINGS, 8, 2,
                      {"enabled": True, "waist_height": 1.12,
                       "lower_coverage": 6, "upper_coverage": 9})
    assert e["band"]["lower"]["liters"] == 6.19
    assert e["band"]["upper"]["liters"] == 6.19
    assert e["band"]["total_liters"] == 12.38
    assert e["liters"] == 12.38

def test_band_per_band_coats():
    e = estimate_room(5, 4, 2.8, OPENINGS, 8, 2,
                      {"enabled": True, "waist_height": 1.12, "lower_coverage": 6,
                       "upper_coverage": 9, "upper_coats": 1})
    assert e["band"]["lower"]["coats"] == 2
    assert e["band"]["upper"]["coats"] == 1
    assert e["band"]["upper"]["liters"] == 3.09

def test_band_off_identical_to_base():
    base = estimate_room(5, 4, 2.8, OPENINGS, 8, 2)
    assert estimate_room(5, 4, 2.8, OPENINGS, 8, 2, None) == base
    assert estimate_room(5, 4, 2.8, OPENINGS, 8, 2, {"enabled": False}) == base

@pytest.mark.parametrize("waist", [0, -0.5, 2.8, 3.1])
def test_bad_waist_rejected(waist):
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, OPENINGS, 8, 2,
                      {"enabled": True, "waist_height": waist,
                       "lower_coverage": 6, "upper_coverage": 9})

@pytest.mark.parametrize("lc,uc", [(0, 9), (-1, 9), (6, 0), (6, -2)])
def test_bad_band_coverage_rejected(lc, uc):
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, OPENINGS, 8, 2,
                      {"enabled": True, "waist_height": 1.12,
                       "lower_coverage": lc, "upper_coverage": uc})
