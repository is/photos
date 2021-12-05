import xml.etree.ElementTree as ET


def et_to_dict(root):
    dict = {}
    for node in root:
        if node.tag == 'key':
            key = node.text
        elif node.tag == 'dict':
            value = et_to_dict(node)
            dict[key] = value
        elif node.tag == 'integer':
            value = int(node.text)
            dict[key] = value
    return dict


def plist_file_to_dict(fn):
    tree = ET.parse(fn)
    return et_to_dict(tree.getroot()[0])


if __name__ == '__main__':
    d = plist_file_to_dict('IDCLabelInfo.xml')
    print(d)