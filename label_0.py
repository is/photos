import sys
import os
import xml.etree.ElementTree as ET

def get_file_list(fn):
    fns = []
    tree = ET.parse(fn)
    root = tree.getroot()
    level0 = root[0]
    for node in level0:
        if node.tag == 'key':
            fns.append(node.text)
    return fns


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        idc_fn = sys.argv[1]
    elif os.path.isfile('IDCLabelInfo.xml'):
        idc_fn = 'IDCLabelInfo.xml'
    fns = get_file_list(idc_fn)
    for fn in fns:
        print(f'mv {fn} ../KEEP')

