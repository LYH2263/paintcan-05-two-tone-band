"""墙腰双色分带（two-tone banding）。

按腰线离地高度把四面墙的净面积（开洞已在总面积上扣过一次）切成下带与上带，
切分只按高度比例进行，不再对开洞做任何二次扣除。
"""

import math


class BandError(ValueError):
    """分带入参非法（腰线越界等），整单拒绝。"""


def split_net(net_m2, height, waist_height):
    """净面积按腰线高度比例切为 (下带, 上带)。

    腰线高度必须严格位于 (0, 层高) 之间，否则抛 BandError。
    """
    if waist_height is None:
        raise BandError("分带开启时必须给出腰线高度")
    h = float(height)
    w = float(waist_height)
    if not (math.isfinite(h) and math.isfinite(w)) or w <= 0 or w >= h:
        raise BandError("腰线高度必须大于 0 且小于层高")
    lower = float(net_m2) * w / h
    upper = float(net_m2) * (h - w) / h
    return lower, upper
