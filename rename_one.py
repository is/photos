import sys
import rename_arw
import os

def rename_one(path):
    print(path)
    for root, dirs, files in os.walk(path):
        renames = []
        rename_map = {}
        taginfos = {}
        for file in files:
            if file[0] == '.':
                continue

            basename, _, ext = file.rpartition('.')
            if basename not in rename_map:
                if basename.startswith('a6400_'):
                    new_name = basename.replace('a6400_', 'a_')
                    rename_map[basename] = new_name
                    renames.append((basename, new_name))
                if basename.startswith('a7r4_'):
                    new_name = basename.replace('a7r4_', 'A_')
                    rename_map[basename] = new_name
                    renames.append((basename, new_name))

            if file.find('__') != -1:
                continue

            full_path = os.path.join(root, file)
            if ext.lower() == 'arw':
                tags = rename_arw.image_exif_tags(full_path)
                if not basename in taginfos:
                    taginfos[basename] = tags
                    new_name = rename_arw.exif_to_filename(taginfos[basename])
                    rename_map[basename] = new_name
                    renames.append((basename, new_name))

        for file in files:
            basename, _, ext = file.rpartition('.')
            if basename not in rename_map:
                continue
            new_name = rename_map[basename]
            print(f'''{root}/{basename}.{ext} => {new_name}.{ext}''')
            os.rename(f'{root}/{basename}.{ext}', 
                f'{root}/{new_name}.{ext}')

def main():
    path = sys.argv[1]
    rename_one(path)

if __name__ == '__main__':
    main()
