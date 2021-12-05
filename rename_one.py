import sys
import rename_arw
import os

def rename_one(path):
    print(path)
    for root, dirs, files in os.walk(path):
        taginfos = {}
        for file in files:
            if file.find('__') != -1:
                continue
            full_path = os.path.join(root, file)
            basename, _, ext = file.rpartition('.')
            if ext.lower() == 'arw':
                tags = rename_arw.image_exif_tags(full_path)
                taginfos[basename] = tags

        for file in files:
            basename, _, ext = file.rpartition('.')
            if basename not in taginfos:
                continue
            new_name = rename_arw.exif_to_filename(taginfos[basename])
            print(f'''{root}/{basename}.{ext} => {new_name}.{ext}''')
            os.rename(f'{root}/{basename}.{ext}', 
                f'{root}/{new_name}.{ext}')

def main():
    path = sys.argv[1]
    rename_one(path)

if __name__ == '__main__':
    main()