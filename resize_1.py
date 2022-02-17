import os
import sys
import glob

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from point_2d import Point2D as P, Rect as R

IMG_DIR = '/Users/is/P3/JPEG'
FONT_0_FN = 'font/ubuntu/Ubuntu-C.ttf'
# fn = '/Users/is/P3/JPEG/A_02189__20220210_133505.jpg'


def gen_image_list(dir):
    pairs = []
    fns = glob.glob(os.path.join(dir, '*.*'))
    for fn in fns:
        basename = os.path.basename(fn)
        name, ext = os.path.splitext(basename)
        lext = ext.lower()
        if lext not in ('.jpeg', '.jpg'):
            continue

        if name.endswith('__'):
            continue

        pfn = fn.replace(ext, "__" + ext)
        if pfn in fns:
            continue
        pairs.append((fn, pfn))

    return pairs

def calc_size(shape, max_size):
    w, h = shape
    if w > h:
        side = 'w'
        rate = 1.0 * max_size / w
    else:
        side = 'h'
        rate = 1.0 * max_size / h
    return (int(w * rate), int(h * rate))

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
}

def watermark_is_0(img, **kwargs):
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
    draw.rounded_rectangle(r, fill=bg, radius=C['radius']*g)
    draw.text(base_center, text,
        anchor='mm', font=font_0, fill=fg)
    p1 = P(0, draw_size[1] - C['bottum_width'] * g)
    draw.rectangle((p1, draw_size- (1,1)), fill=bg)
    l0 = l0.resize(img.size, resample=Image.LANCZOS)
    img = Image.alpha_composite(img, l0)
    return img


def sub_rect_light(img, rect):
    im_corp = img.crop((rect[0][0], rect[0][1], rect[1][0], rect[1][1]))
    im_gray = im_corp.convert('L')
    return int(np.mean(np.asarray(im_gray)))


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
    #print('light')
    #print(sub_rect_light(img, r0))
    bg_light = sub_rect_light(img, r0)
    print(bg_light)
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


def process(infn, outfn):
    im = Image.open(infn)
    exif = im.info['exif']
    new_size = calc_size(im.size, 1920)
    print(f'''{infn} -> {os.path.basename(outfn)} : {im.size} -> {new_size}''')
    out = im.resize(new_size, resample=Image.LANCZOS)
    out = out.convert('RGBA')
    out = watermark_is_1(out, text='IS')
    out = out.convert('RGB')
    out.save(outfn, quality=100, subsampling=0, exif=exif)


# ---
def main():
    img_dir = IMG_DIR
    if len(sys.argv) > 1:
        img_dir = sys.argv[1]
    imgs = gen_image_list(img_dir)
    for pair in imgs:
        process(pair[0], pair[1])

def main1():
    process('DSC01952.jpg', 'out.jpg')

if __name__ == '__main__':
    main()

