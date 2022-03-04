import math
from typing import Sequence, Tuple, Union
from point_2d import Point2D as P, Rect as R

# 
#  0  1  2
#  7     3
#  6  5  4
def affix_to_border(box:P, off:P) -> Sequence[P]:
    w, h = box
    w = int(w)
    h = int(h)
    cw = w // 2
    ch = h // 2
    w = w - 1
    h = h - 1
    ow, oh = off
    return (
        P(ow, oh), P(cw, oh), P(w - ow, oh), P(w - ow, ch),
        P(w - ow, h - oh), P(cw, h - oh), P(ow, h - oh), P(ow, ch))


def align_n(num:int, base:int) -> int:
    return int(math.floor((num / base) + 0.5) * base)

def calc_size(shape:Sequence[int], max_size:int) -> Tuple[int, int]:
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