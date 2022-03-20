import os
import math
import glob
import glob

from typing import Sequence, Tuple, Union
from point_2d import Point2D as P, Rect as R

import numpy as np
from PIL import Image, ImageDraw, ImageFont


IMG_DIR = '/Users/is/P3/JPEG'

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
    if (rate >= 1.0):
        return (w, h)
    wnew = int(shape[0] * rate)
    hnew = int(shape[1] * rate)
    wnew = align_n(wnew, 4)
    hnew = align_n(hnew, 4)
    return (wnew, hnew)


# -- 判断是否是原始文件
def is_origin_path(fn:str) -> bool:
    basename = os.path.basename(fn)
    name, ext = os.path.splitext(basename)
    if name[-3:-1] == '__':
        return False
    if name.endswith('__preview'):
        return False
    return True


# -- 构建文件列表
def gen_image_list(dir:str, postfix:str) -> Sequence[Tuple[str, str]]:
    pairs = []
    fns = glob.glob(os.path.join(dir, '*.*'))
    for fn in fns:
        basename = os.path.basename(fn)
        name, ext = os.path.splitext(basename)
        lext = ext.lower()
        if lext not in ('.jpeg', '.jpg'):
            continue

        if not is_origin_path(fn):
            continue

        if name[-3:-1] == '__':
            continue

        pfn = fn.replace(ext, postfix + ext)
        if pfn in fns:
            continue
        pairs.append((fn, pfn))

    return pairs


# ---
# --
def border(img, border_width=5, border_color=(255, 255, 255, 128)):
    background = img.convert('RGBA')
    border =  Image.new('RGBA', img.size, border_color)
    draw = ImageDraw.Draw(border)
    w, h = img.size
    draw.rectangle((border_width, border_width, w - border_width, h - border_width),
        fill=(255, 255, 255, 0), )
    out = Image.alpha_composite(background, border)
    return out.convert('RGB')


IS_STYLE_DEFAULT_CFG = {
    'text': 'IS',
    'gain': 5,
    'logo_offset': (50, 50),
    'font_size': 45,
    'bottum_width': 10,
    'bgcolor': (255, 255, 255, 128),
    'fgcolor': (32, 32, 32, 16),
    'radius': 35,
    'padding': 15,
    'paddingx': 8,
    'logo_image_path': 'img/logo_is_720__0.png',
    'logo_size': (72, 72)
}


def sub_rect_light(img, rect):
    im_corp = img.crop((rect[0][0], rect[0][1], rect[1][0], rect[1][1]))
    im_gray = im_corp.convert('L')
    return int(np.mean(np.asarray(im_gray)))


def watermark_is_2(ctx, img, **kwargs):
    C = dict(IS_STYLE_DEFAULT_CFG)
    C.update(kwargs)
    draw_size = P(img.size)
    img_mask = Image.new('RGBA', draw_size, (0,0,0,0))

    logo_img = Image.open(C['logo_image_path'])
    logo_img = logo_img.resize(C['logo_size'], resample=Image.LANCZOS)
    base_offset = P(C['logo_offset'])
    base_center = affix_to_border(draw_size, base_offset)[4]
    r = base_center.center_extend(logo_img.size)

    bg_light = sub_rect_light(img, r)
    # print(bg_light)
    border_color = C['bgcolor']
    if bg_light >= 140:
        arr = np.array(logo_img)
        arr[:,:,0:3] = 255 - arr[:,:,0:3]
        logo_img = Image.fromarray(arr)
    
    img_mask.paste(logo_img, (int(r[0][0]), int(r[0][1])))
    p1 = P(0, draw_size[1] - C['bottum_width'])
    draw = ImageDraw.Draw(img_mask)
    draw.rectangle((p1, draw_size-(1,1)), fill=border_color)
    #l0 = l0.resize(img.size, resample=Image.LANCZOS)
    img = Image.alpha_composite(img, img_mask)
    return img



def watermark_is_1(img, **kwargs):
    C = dict(IS_STYLE_DEFAULT_CFG)
    C.update(kwargs)

    text = C['text']
    g = C['gain']
    bg = C['bgcolor']
    fg = C['fgcolor']

    base_size = P(img.size)
    draw_size = base_size * g
    l0 = Image.new('RGBA', draw_size, (0,0,0,0))
    draw = ImageDraw.Draw(l0)
    font_0 = ImageFont.truetype(
        FONT_0_FN, C['font_size'] * g, 
        layout_engine=ImageFont.LAYOUT_RAQM)
    font_size = draw.textsize(text, font = font_0)
    font_size = P(font_size)
    base_offset = P(C['logo_offset']) * g
    base_center = draw_size - base_offset
    r = base_center.center_extend(font_size)
    r = r.center_extend(P(C['padding']) * g).center_extend(P(C['paddingx'], 0) * g)

    r0 = R(r[0] / g, r[1] / g)
    # print('light')
    # print(sub_rect_light(img, r0))
    bg_light = sub_rect_light(img, r0)
    # print(bg_light)
    border_color = bg
    if bg_light >= 190:
        bg = (255-bg[0], 255-bg[1], 255-bg[2], bg[3])
        fg = (255-fg[0], 255-fg[1], 255-fg[2], fg[3])

    draw.rounded_rectangle(r, fill=bg, radius=C['radius']*g)
    draw.text(base_center, text,
        anchor='mm', font=font_0, fill=fg)
    p1 = P(0, draw_size[1] - C['bottum_width'] * g)
    draw.rectangle((p1, draw_size- (1,1)), fill=border_color)
    l0 = l0.resize(img.size, resample=Image.LANCZOS)
    img = Image.alpha_composite(img, l0)
    return img



# ---
def crop_to_square(img):
    w, h = img.size
    if w == h:
        return img
    if w > h:
        box = ((w - h) / 2, 0, (w + h) / 2, h)
    else:
        box = (0, (h - w) / 2, w, (h + w) / 2)
    return img.crop(box)