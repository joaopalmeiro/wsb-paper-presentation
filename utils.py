from math import ceil, log10
import string
import pandas as pd
from typing import List


def log10_ceiling(x: int) -> int:
    return 10 ** (ceil(log10(x)))


def load_data(v: List[int] = [1, 600, 6_000, 300, 10, 1_000, 80, 4]) -> pd.DataFrame:
    c = list(string.ascii_uppercase)[: len(v)]
    data = pd.DataFrame({"category": c, "value": v, "scale": map(log10_ceiling, v)})

    return data
