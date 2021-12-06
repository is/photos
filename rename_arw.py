import os
import exifread


def exif_to_filename(tags):
    #print(tags['Image Model'])
    #print(tags['Image DateTime'])
    model = tags['Image Model']
    ts = tags['Image DateTime']
    if model.values == 'ILCE-6400':
        model = 'a'
    else:
        model = 'A'
    ts = ts.values.replace(':', '').replace(' ', '_')

    basename = os.path.basename(tags['__source'])
    basename, _, ext = basename.rpartition('.')
    if len(basename) == 8:
        return f'{model}_{basename[3:]}__{ts}'
    return f'{model}__{ts}'


def image_exif_tags(fn):
    with open(fn, 'rb') as fin:
        tags = exifread.process_file(fin)
        tags['__source'] = fn
    return tags

def new_file(full_path, tags=None):
    basename = os.path.basename(full_path)
    dirname = os.path.dirname(full_path)
    main, _, ext = basename.rpartition('.')
    if tags == None:
        tags = image_exif_tags(full_path)
    new_fn = exif_to_filename(tags)
    basename = os.path.basename(tags['__source'])
    basename, _, ext = basename.rpartition('.')
    if len(basename) == 8:
        return os.path.join(dirname, f'{new_fn}_{basename[3:]}.{ext}')
    return os.path.join(dirname, f'{new_fn}.{ext}')
    


if __name__ == '__main__':
    tags = image_exif_tags('A6A07502.ARW')
    #print(exif_to_filename(tags))
    print(new_file('A6A07502.ARW', tags))
