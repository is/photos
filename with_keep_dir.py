"""
输出存在对应KEEP目录的目录
"""
import sys
import os
import glob

def list_with_keep_dir(basepath):
    r = []
    paths = glob.glob(f'{basepath}/*')
    pset = set(paths)
    for path in paths:
        if '__KEEP_' in path:
            continue
        if '__' in path:
            pair_path = path.replace('__', '__KEEP_')
            if pair_path in pset:
                r.append(path)
    return r

def main():
    if len(sys.argv) >= 2:
        os.chdir(sys.argv[1])
    dirs = list_with_keep_dir(".")
    dirs.sort()
    for d in dirs:
        print(d)

if __name__ == '__main__':
    main()