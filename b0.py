import sys
import os
import argparse
import glob
import re
import logging

# --
HOME = os.environ['HOME']

IN_DIR = f'{HOME}/P1_IN'
HOLD_DIR = f'{HOME}/P1_HOLD'
KEEP_DIR = f'{HOME}/P1'


# --
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)
L = logging.getLogger('main')
L.setLevel(logging.INFO)
L.addHandler(console_handler)

# --
def gen_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dryrun', '-d', help='dry run',
        action='store_true')
    parser.add_argument('--verbose', '-v', help='verbose mode',
        action="store_true")
    parser.add_argument('src', help='NEF source directory')
    return parser

def main():
    parser = gen_argparser()
    args = parser.parse_args()
    
    dryrun = (args.dryrun == True)
    # dryrun = True
    
    if args.verbose == True:
        L.setLevel(logging.DEBUG)

    if not os.path.isdir(args.src):
        print(f'{args.src} is not directory!')
        return
    
    src_dir = args.src
    date_str = os.path.basename(src_dir)
    if re.match(r'\d{8}', date_str) == None:
        print(f'{args.src} must be a date')
        return

    dest_dir = os.path.join(KEEP_DIR, date_str)


    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    move_set = set()

    fset_xmp = glob.glob(f"{src_dir}/*.xmp")
    fset_xmp.sort()
    for fn in fset_xmp:
        rate, ext = get_info_from_xmp(fn)
        fn_raw = fn.replace('.xmp', f'.{ext}')
        base_fn_raw = os.path.basename(fn_raw)
        dest_fn_raw = os.path.join(dest_dir, base_fn_raw)
        
        # print(f'{fn} {rate}')
        if rate > 0:
            do_rename(fn_raw, dest_fn_raw, True, dryrun)
            move_set.add(fn_raw)

    keep_set = set(move_set)

    dest_dir = os.path.join(HOLD_DIR, date_str)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    fset_xmp = glob.glob(f"{src_dir}/*.xmp")
    fset_xmp.sort()    
    for fn in fset_xmp:
        rate, ext = get_info_from_xmp(fn)
        fn_raw = fn.replace('.xmp', f'.{ext}')
        if fn_raw in move_set:
            continue
        base_fn_raw = os.path.basename(fn_raw)
        dest_fn_raw = os.path.join(dest_dir, base_fn_raw)
        do_rename(fn_raw, dest_fn_raw, True, dryrun)
        move_set.add(fn_raw)

    fset_raw = glob.glob(f"{src_dir}/*.NEF")
    fset_raw.sort()
    for fn in fset_raw:
        if fn in move_set:
            continue
        base_fn_raw = os.path.basename(fn)
        dest_fn_raw = os.path.join(dest_dir, base_fn_raw)
        do_rename(fn, dest_fn_raw, False, dryrun)
        move_set.add(fn)

    fset_raw = glob.glob(f"{src_dir}/*.ARW")
    fset_raw.sort()
    for fn in fset_raw:
        if fn in move_set:
            continue
        base_fn_raw = os.path.basename(fn)
        dest_fn_raw = os.path.join(dest_dir, base_fn_raw)
        do_rename(fn, dest_fn_raw, False, dryrun)
        move_set.add(fn)

    move_keep = len(keep_set)
    move_hold = len(move_set) - move_keep
    L.info(f"KEEP:{move_keep}, HOLD:{move_hold}")


def do_rename(src, dest, with_xmp, dryrun):
    if not os.path.isfile(dest):
        if dryrun:
            L.info(f'move {src} to {dest}')
        else:
            os.rename(src, dest)
    else:
        L.debug(f'{dest} is existed')

    if not with_xmp:
        return
    
    if src.endswith('.NEF'):
        src = src.replace('.NEF', '.xmp')
        dest = dest.replace('.NEF', '.xmp')
    elif src.endswith('.ARW'):
        src = src.replace('.ARW', '.xmp')
        dest = dest.replace('.ARW', '.xmp')
        
    if not os.path.isfile(dest):
        if dryrun:
            L.info(f'move {src} to {dest}')
        else:
            os.rename(src, dest)
    else:
        L.debug(f'{dest} is existed')

# --
def get_info_from_xmp(fn):
    with open(fn) as f:
        xmp = f.read()
    match = re.search(r'''xmp:Rating="(\d+)"''', xmp)
    if match == None:
        rating = 0
    else:
        rating = int(match.group(1))
    
    match = re.search(r'''photoshop:SidecarForExtension="(.+?)"''', xmp)
    if match == None:
        ext = 'XXX'
    else:
        ext = match.group(1)
    return rating, ext

# --
def read_rating(fn):
    with open(fn) as f:
        xmp = f.read()
    match = re.search(r'''xmp:Rating="(\d+)"''', xmp)
    if match == None:
        return 0
    return int(match.group(1))

if __name__ == '__main__':
    main()
