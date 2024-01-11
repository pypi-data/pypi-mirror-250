import random

from typing import List


def rgb_to_hex(rgb: List[int]) -> str:
    hex_str = "#"
    for i in rgb:
        int_to_hex = str(hex(int(i))[2:])
        if len(int_to_hex) == 0:
            raise ValueError(f"hex invalid: {int_to_hex}")
        elif len(int_to_hex) == 1:
            int_to_hex = f"0{int_to_hex}"
        elif len(int_to_hex) > 2:
            int_to_hex = int_to_hex[:2]
        hex_str += int_to_hex
    return hex_str


def hsl_to_rgb(hsl: List[float]) -> List[int]:
    def color_c(_p: float, _q: float, t: float):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < (1 / 6):
            return _p + (_q - _p) * 6 * t
        if t < .5:
            return _q
        if t < (2 / 3):
            return _p + (_q - _p) * 6 * (2 / 3 - t)
        return _p

    if (not hsl) or (len(hsl) != 3):
        raise ValueError(f"hsl invalid: {hsl}")
    h, s, l = hsl
    r = g = b = l
    if s != 0:
        q = (l * (1 + s)) if (l < .5) else (l + s - l * s)
        p = 2 * l - q
        h = h / 360
        r = color_c(p, q, h + (1 / 3))
        g = color_c(p, q, h)
        b = color_c(p, q, h - (1 / 3))
    return [int(r * 255), int(g * 255), int(b * 255)]


def random_hsl(base_hsl: List[float] = None) -> List[float]:
    if base_hsl is None:
        raise ValueError(f"base hsl invalid: {base_hsl}")
    hsl = [random.randint(0, 360), random.random(), random.random()]
    while (len(base_hsl) > 0) and (abs(hsl[0] - base_hsl[0]) < 0.25):
        hsl[0] = random.randint(0, 360)
    hsl[1] = 0.7 + (hsl[1] * 0.2)
    hsl[2] = 0.4 + (hsl[2] * 0.4)
    hsl = list(map(lambda x: float("%.2f" % x), hsl))
    return hsl


def random_color_array(number: int, color_type: str = "rgb") -> List[float or int or str]:
    color_array = []
    last_hsl = []
    for i in range(number):
        hsl = random_hsl(last_hsl)
        last_hsl = hsl
        if color_type == "hsl":
            color_array.append(hsl)
        elif color_type == "rgb":
            color_array.append(hsl_to_rgb(hsl))
        elif color_type == "hex":
            color_array.append(rgb_to_hex(hsl_to_rgb(hsl)))

    return color_array


if __name__ == "__main__":
    color = random_color_array(50, "hex")
    print(color)