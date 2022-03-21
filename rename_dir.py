import sys
import os
import glob

import rename_common
import rename_common as common
import rename_common as co


def rename_one(path):
    print(path)
    for root, dirs, files in os.walk(path):
        files = sorted(files)
        renames = []
        rename_map = {}
        taginfos = {}

        if root.split('/')[-1] == 'preview':
            continue

        for file in files:
            if file[0] == '.':
                continue

            basename, _, ext = file.rpartition('.')
            if basename not in rename_map:
                if basename.startswith('a6400_'):
                    new_name = basename.replace('a6400_', 'B_')
                    rename_map[basename] = new_name
                    renames.append((basename, new_name))
                elif basename.startswith('a_'):
                    new_name = basename.replace('a_', 'B_')
                    rename_map[basename] = new_name
                    renames.append((basename, new_name))
                elif basename.startswith('a7r4_'):
                    new_name = basename.replace('a7r4_', 'A_')
                    rename_map[basename] = new_name
                    renames.append((basename, new_name))

            if file.find('__') != -1:
                continue

            full_path = os.path.join(root, file)
            if basename in rename_map:
                continue

            new_name = None
            if ext.lower() == 'arw':
                _, new_name = common.rename__arw(full_path)

            if ext.lower() in ('jpg', 'jpeg'):
                _, new_name = common.rename__jpg(full_path)

            if ext.lower() in ('heif', 'heic'):
                _, new_name = common.rename__heif(full_path)


            if (new_name != None and new_name != basename):
                rename_map[basename] = new_name
                renames.append((basename, new_name))
                print(f'-> {full_path} -> {new_name}')


        if len(renames) != 0:
            with open(os.path.join(root, ".rename.csv"), 'wb') as cout:
                cout.write("\n".join([f'{a[0]},{a[1]}' for a in renames]).encode('utf8'))
                cout.write("\n".encode('utf8'))

        for file in files:
            basename, _, ext = file.rpartition('.')
            if basename not in rename_map:
                continue
            new_name = rename_map[basename]
            print(f'''{root}/{basename}.{ext} => {new_name}.{ext}''')
            os.rename(f'{root}/{basename}.{ext}', 
                f'{root}/{new_name}.{ext}')

        if os.path.isdir(os.path.join(root, 'preview')):
            for filepath in glob.glob(f'{root}/preview/*'):
                file = os.path.basename(filepath)
                basename, _, ext = file.rpartition('.')
                if basename not in rename_map:
                    continue
                new_name = rename_map[basename]
                print(f'''{root}/preview/{basename}.{ext} => preview/{new_name}.{ext}''')
                os.rename(f'{root}/preview/{basename}.{ext}',
                    f'{root}/preview/{new_name}.{ext}')


def main():
    path = sys.argv[1]
    rename_one(path)

if __name__ == '__main__':
    main()
