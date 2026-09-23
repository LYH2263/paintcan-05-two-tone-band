from app.engines.paint_volume import paint_liters
from app.engines.wall_area import wall_area
from app.modules.two_tone_band import BandError, split_net


def estimate_room(length, width, height, openings, coverage, coats,
                  band=False, waist_height=None,
                  lower_coverage=None, lower_coats=None,
                  upper_coverage=None, upper_coats=None):
    area = wall_area(length, width, height, openings)
    net = area["net_m2"]
    if not band:
        # 分带缺省关闭：升数与改造前同房同参完全一致
        vol = paint_liters(net, coverage, coats)
        return {**area, **vol, "band": False}

    # 开洞已在总面积上扣除一次（wall_area），这里只按带高比例切净面积
    lower_area, upper_area = split_net(net, height, waist_height)
    lower_area = round(lower_area, 2)
    upper_area = round(net - lower_area, 2)  # 两带面积展示值可加回净面积
    lower = paint_liters(lower_area, lower_coverage, lower_coats)
    upper = paint_liters(upper_area, upper_coverage, upper_coats)
    total = round(lower["liters"] + upper["liters"], 2)
    return {
        **area,
        "band": True,
        "waist_height": round(float(waist_height), 2),
        "lower_band": {
            "net_m2": lower_area,
            "liters": lower["liters"],
            "coats": lower["coats"],
            "coverage": lower["coverage"],
        },
        "upper_band": {
            "net_m2": upper_area,
            "liters": upper["liters"],
            "coats": upper["coats"],
            "coverage": upper["coverage"],
        },
        "liters": total,
    }
