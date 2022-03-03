import math
from typing import Sequence


def align_n(num:int, base:int) -> int:
    return int(math.floor((num / base) + 0.5) * base)

def calc_size(shape:Sequence[int], max_size:int) -> (int, int):
    w, h = shape
    if w > h:
        side = 'w'
        rate = 1.0 * max_size / w
    else:
        side = 'h'
        rate = 1.0 * max_size / h
    wnew = int(shape[0] * rate)
    hnew = int(shape[1] * rate)
    wnew = align_n(wnew, 4)
    hnew = align_n(hnew, 4)
    return (wnew, hnew)