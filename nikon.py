import sys
import os
import binascii
import glob
import shutil

import xml.etree.ElementTree as ET

from pydantic import BaseModel

NS_MAP = {
    'ast': 'http://ns.nikon.com/asteroid/1.0/',
    'xmp': 'http://ns.adobe.com/xap/1.0/',
}

# ---
class NikonMeta(BaseModel):
    fn: str = '_'
    label: str = 'UNSET'
    rating: str = 'UNSET'


# ---
def read_nikon_meta(fn:str) -> NikonMeta:
    print(fn)
    tree_0 = ET.parse(fn)
    root_0 = tree_0.getroot()

    xmp_node = root_0[0][0].find('ast:XMLPackets', namespaces=NS_MAP)
    if xmp_node == None:
        return NikonMeta(fn=os.path.basename(fn))
    xmp_text = root_0[0][0].find('ast:XMLPackets', namespaces=NS_MAP)[0].text
    xmp_body = binascii.a2b_base64(xmp_text).decode('utf-8')
    xmp_root = ET.fromstring(xmp_body)

    rdf_1 = xmp_root[0][0]
    label = 'UNSET'
    label_node = rdf_1.find('xmp:Label', namespaces=NS_MAP)
    if label_node != None:
        label = label_node.text
    
    rating = 'UNSET'
    rating_node = rdf_1.find('xmp:Rating', namespaces=NS_MAP)
    if rating_node != None:
        rating = rating_node.text

    # print(f'META: {fn} {label} {rating}')
    return NikonMeta(
        fn=os.path.basename(fn),
        label=label,
        rating=rating)


def scan_nksc_param_dir(path:str) -> list[NikonMeta]:
    fns = glob.glob(f'{path}/NKSC_PARAM/*.nksc')
    fns.sort()
    return [read_nikon_meta(fn) for fn in fns]


def nikon_s1(src:str, dest:str):
    os.makedirs(f'{dest}/NKSC_PARAM', exist_ok=True)
    metas = scan_nksc_param_dir(src)
    copy_set = {}
    for meta in metas:
        if meta.rating != 'UNSET' or meta.label != 'UNSET':
            id = meta.fn.partition('.')[0]
            copy_set[id] = id

    for id in copy_set.keys():
        if not os.path.exists(f'{dest}/{id}.NEF'):
            try:
                shutil.copy2(f'{src}/{id}.NEF', f'{dest}/{id}.NEF')
            except FileNotFoundError as E:
                pass
        if not os.path.exists(f'{dest}/{id}.JPG'):
            shutil.copy2(f'{src}/{id}.JPG', f'{dest}/{id}.JPG')

        shutil.copy2(f'{src}/NKSC_PARAM/{id}.NEF.nksc',
            f'{dest}/NKSC_PARAM/{id}.NEF.nksc')
        shutil.copy2(f'{src}/NKSC_PARAM/{id}.JPG.nksc',
            f'{dest}/NKSC_PARAM/{id}.JPG.nksc')

if __name__ == '__main__':
    # scan_nksc_param_dir(f'{os.environ["HOME"]}/Z0/NIKON/007')
    nikon_s1(f'{os.environ["HOME"]}/Z0/NIKON/20240518',
        f'{os.environ["HOME"]}/Z0/NI')

