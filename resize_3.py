import os
import sys
import glob

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from point_2d import Point2D as P, Rect as R

import resize_common
import resize_common as common
from resize_common import calc_size, is_origin_path

IMG_DIR = '/Users/is/P0/JPEG'

def process(infn, outfn):
    ctx = {}
    im = Image.open(infn)
    exif = im.info['exif']
    new_size = calc_size(im.size, 768)
    print(f'''{infn} -> {os.path.basename(outfn)} : {im.size} -> {new_size}''')
    out = im.resize(new_size, resample=Image.LANCZOS)
    #out = out.convert('RGBA')
    #out = common.watermark_is_2(ctx, out, text='IS')
    out = out.convert('RGB')
    out.save(outfn, quality=100, subsampling=0, exif=exif)


# ---
def main():
    img_dir = IMG_DIR
    if len(sys.argv) > 1:
        img_dir = sys.argv[1]
    imgs = common.gen_image_list(img_dir, "__preview")
    for pair in imgs:
        process(pair[0], pair[1])


if __name__ == '__main__':
    main()

