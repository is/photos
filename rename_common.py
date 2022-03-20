import os
import exifread

from PIL import Image, ExifTags
import pyheif
from typing import Tuple

# === ARW ===
def arw_image_exif_tags(fn):
    with open(fn, 'rb') as fin:
        tags = exifread.process_file(fin)
        tags['__source'] = fn
    return tags


def arw_exif_to_basename(full_path, tags):
    model = tags['Image Model']
    ts = tags['Image DateTime']
    if model.values == 'ILCE-6400':
        model = 'B'
    else:
        model = 'A'
    ts = ts.values.replace(':', '').replace(' ', '_')

    basename = os.path.basename(full_path)
    basename, _, ext = basename.rpartition('.')
    if len(basename) == 8:
        return f'{model}_{basename[3:]}__{ts}'
    return f'{model}__{ts}'


def rename__arw(full_path:str) -> Tuple[str, str]:
    tags = arw_image_exif_tags(full_path)
    basename = os.path.basename(full_path)
    dirname = os.path.dirname(full_path)
    new_fn = arw_exif_to_basename(full_path, tags)
    basename, _, ext = basename.rpartition('.')
    new_full_path = full_path.replace(basename, new_fn)
    return (new_full_path, new_fn)


# === JPG
def new_basename_with_ts(basename, ts):
    ts = ts.replace(' ', '_').replace(':', '')
    new_name = f'{basename}__{ts}';
    new_name = new_name.replace('IMG_', 'I_0')
    new_name = new_name.replace('DSC', 'I_')
    return new_name


def rename__jpg(full_path:str) -> Tuple[str, str]:
    basename = os.path.basename(full_path)
    basename, _, ext = basename.rpartition('.')
    img = Image.open(full_path)
    exif = img._getexif()
    if not exif:
        return (full_path, basename)
    if 36868 not in exif:
        return (full_path, basename)
    ts = exif[36868]
    new_name = new_basename_with_ts(basename, ts)
    new_full_path = full_path.replace(basename, new_name)
    return (new_full_path, new_name)



# === HEIF/HEIC
def rename__heif(full_path:str) -> Tuple[str, str]:
    basename = os.path.basename(full_path)
    basename, _, ext = basename.rpartition('.')
    img = pyheif.read_heif(full_path, False)
    ts = None
    for meta in img.metadata:
        print(meta['type'])
        if meta['type'] == 'Exif':
            exif = Image.Exif()
            exif.load(meta['data'])
            ts = exif._get_merged_dict()[36868]
            ts = ts.replace(' ', '_').replace(':', '')
            break
    
    if ts == None:
        return (full_path, basename)
    new_name = new_basename_with_ts(basename, ts)
    new_full_path = full_path.replace(basename, new_name)
    return (new_full_path, new_name)


if __name__ == '__main__':
    # print(rename__jpg('DSC01952.jpg'))
    print(rename__heif('IMG_5678.HEIC'))