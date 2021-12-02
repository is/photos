import os
import json

import rawpy
import imageio


def read_config(fn):
    with open(fn) as f:
        return json.load(f)


def dst_path(src, dst, p, ext):
    p = p.replace(src, dst)
    p, _, _ = p.rpartition('.')
    return f'{p}.{ext}'

def scan_raw(src):
    R = []
    for root, dirs, files in os.walk(src, topdown=False):
        for f in files:
            fn = f.lower()
            if fn.startswith('._'):
                continue
            if fn.endswith('.arw') or fn.endswith('.raw'):
                R.append(os.path.join(root, f))
    return R


def scan_raw_to_jpg(src, dst):
    raw_fns = scan_raw(src)
    dst_big = os.path.join(dst, 'big')
    dst_small = os.path.join(dst, 'small')

    c = len(raw_fns) + 1
    for fn in raw_fns:
        c = c - 1
        jpg_fn = dst_path(src, dst_big, fn, 'jpg')
        if os.path.exists(jpg_fn):
            print(f'skip {fn}')
            continue

        jpg_dir = os.path.dirname(jpg_fn)
        if not os.path.isdir(jpg_dir):
            print(f'mkdir {jpg_dir}')
            os.makedirs(jpg_dir)

        print(f'conv {c} . {fn} -> {jpg_fn}')
        convert_raw_to_jpg(fn, jpg_fn)


def convert_raw_to_jpg(ifn, ofn):
    with rawpy.imread(ifn) as raw:
        rgb = raw.postprocess(gamma=(1,1))
        imageio.imsave(ofn, rgb)


def main():
    C = read_config('cf.json')
    dst = C['dst']
    for src in C['src']:
        print(src)
        scan_raw_to_jpg(src, dst)


if __name__ == '__main__':
    main()

# vim: ts=4 sts=4 expandtab ai
