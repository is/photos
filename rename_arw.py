import os
import exifread


def exif_to_filename(tags):
    #print(tags['Image Model'])
    #print(tags['Image DateTime'])
    model = tags['Image Model']
    ts = tags['Image DateTime']
    if model.values == 'ILCE-6400':
        model = 'a6400'
    else:
        model = 'a7r4'
    ts = ts.values.replace(':', '').replace(' ', '_')
    return f'{model}__{ts}'


def image_exif_tags(fn):
    with open(fn, 'rb') as fin:
        tags = exifread.process_file(fin)
    return tags

def new_file(full_path, tags=None):
    basename = os.path.basename(full_path)
    dirname = os.path.dirname(full_path)
    main, _, ext = basename.rpartition('.')
    if tags == None:
        tags = image_exif_tags(full_path)
    new_fn = exif_to_filename(tags)
    return os.path.join(dirname, f'{new_fn}.{ext}')
    


if __name__ == '__main__':
    tags = image_exif_tags('A6A07502.ARW')
    #print(exif_to_filename(tags))
    print(new_file('A6A07502.ARW', tags))