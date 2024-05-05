import sys
import os
import binascii
import glob

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
    
    tree_0 = ET.parse(fn)
    root_0 = tree_0.getroot()

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

    print(f'META: {fn} {label} {rating}')
    return NikonMeta(
        fn=os.path.basename(fn),
        label=label,
        rating=rating)


def scan_nksc_param_dir(path:str) -> list[NikonMeta]:
    fns = glob.glob(f'{path}/NKSC_PARAM/*.nksc')
    fns.sort()
    return [read_nikon_meta(fn) for fn in fns]
    

if __name__ == '__main__':
    scan_nksc_param_dir(f'{os.environ["HOME"]}/Z0/NIKON/007')

