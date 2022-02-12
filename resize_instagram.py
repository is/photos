from PIL import Image, ImageDraw, ImageFont

fn = 'DSC01952.jpg'


def calc_size(shape, max_size):
    w, h = shape
    if w > h:
        side = 'w'
        rate = 1.0 * max_size / w
    else:
        side = 'h'
        rate = 1.0 * max_size / h
    return (int(w * rate), int(h * rate))

def border(img, border_width=5, border_color=(255, 255, 255, 128)):
    background = img.convert('RGBA')

    border =  Image.new('RGBA', img.size, border_color)
    draw = ImageDraw.Draw(border)
    w, h = img.size
    draw.rectangle((border_width, border_width, w - border_width, h - border_width),
        fill=(255, 255, 255, 0), )
    out = Image.alpha_composite(background, border)
    return out.convert('RGB')


# ---
def main():
    im = Image.open(fn)
    print(im.format, im.size, im.mode)
    new_size = calc_size(im.size, 1920)
    out = im.resize(new_size)
    out = border(out, border_width=12, border_color=(255, 255, 255, 176))
    # out.save('out.jpg',  quality=100, subsampling=0)
    out.save('out.jpg',  quality=100)

if __name__ == '__main__':
    main()

