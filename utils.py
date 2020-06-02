from math import ceil, log10
import string
import pandas as pd
from typing import List


SUPERSCRIPTS = {
    0: "\u2070",
    1: "\u00B9",
    2: "\u00B2",
    3: "\u00B3",
    4: "\u2074",
    5: "\u2075",
    6: "\u2076",
    7: "\u2077",
    8: "\u2078",
    9: "\u2079",
}


def log10_ceiling(x: int) -> int:
    return 10 ** (ceil(log10(x)))


def numeric_to_mantissa_and_exponent(value):
    exponent = int(len(str(abs(value)).split(".")[0]) - 1)
    mantissa = float(value * 10 ** -exponent)
    multiplier = int(10 ** exponent)

    return mantissa, exponent, multiplier


def end_x(value):
    return 10 * (value + 1)


def load_data(
    v: List[int] = [1, 600, 6_000, 300, 10, 1_000, 80, 4], show_unicode: bool = True
) -> pd.DataFrame:
    c = list(string.ascii_uppercase)[: len(v)]
    data = pd.DataFrame({"category": c, "value": v, "scale": map(log10_ceiling, v)})

    data["mantissa"], data["exponent"], data["multiplier"] = zip(
        *data["value"].map(numeric_to_mantissa_and_exponent)
    )

    data["end"] = data["exponent"].map(end_x)
    data["end"] = data["end"].cumsum()

    data["start"] = data["end"].shift(fill_value=0)

    data["middle"] = ((data["end"] - data["start"]) / 2) + data["start"]

    data["original"] = (
        data["value"].map(str)
        + " = "
        + data["mantissa"].map("{0:g}".format)
        + (
            " × 10^" + data["exponent"].map(str)
            if not show_unicode
            else " × 10" + data["exponent"].map(SUPERSCRIPTS)
        )
    )

    return data
