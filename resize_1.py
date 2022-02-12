import os
import glob

from PIL import Image, ImageDraw

IMG_DIR = '/Users/is/P3/JPEG'
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

def process(infn, outfn):
    im = Image.open(infn)
    new_size = calc_size(im.size, 1920)
    out = im.resize(new_size, resample=Image.LANCZOS)
    # out = border(out, 16, border_color=(255, 255, 255, 239))
    print(f'''{infn} -> {os.path.basename(outfn)} : {im.size} -> {new_size}''')
    out.save(outfn, quality=100, subsampling=0)

# ---
def main():
    imgs = gen_image_list(IMG_DIR)
    for pair in imgs:
        process(pair[0], pair[1])


if __name__ == '__main__':
    main()

