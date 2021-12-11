import xml.etree.ElementTree as ET

def get_file_list(fn):
    fns = []
    tree = ET.parse('IDCLabelInfo.xml')
    root = tree.getroot()
    level0 = root[0]
    for node in level0:
        if node.tag == 'key':
            fns.append(node.text)
    return fns


if __name__ == '__main__':
    fns = get_file_list('IDCLabelInfo.xml')
    for fn in fns:
        print(f'cp {fn} ../KEEP')

