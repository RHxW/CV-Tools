import os
import xml.etree.ElementTree as ET
import json
from tqdm import tqdm

def voc07xmlparser(xml_file):
    if not os.path.exists(xml_file):
        return
    tree = ET.parse(xml_file)
    root = tree.getroot()
    assert root.tag == 'annotation'

    info = dict()
    objs = []
    for elem in root:
        tag = elem.tag
        txt = elem.text
        if tag in ['folder', 'filename', 'segmented']:
            info[tag] = txt
        elif tag == 'object':
            objs.append(innerparser(elem))
        else:
            info[tag] = innerparser(elem)
    info['object'] = objs
    return info


def innerparser(elem):
    inner_dict = dict()
    for sub_elem in elem:
        if sub_elem.tag == 'bndbox':
            inner_dict[sub_elem.tag] = innerparser(sub_elem)
        else:
            inner_dict[sub_elem.tag] = sub_elem.text
    return inner_dict


def voc07xml2json(anno_dir, json_dir):
    assert os.path.exists(anno_dir)
    if anno_dir[-1] != '/':
        anno_dir += '/'
    if json_dir[-1] != '/':
        json_dir += '/'
    if not os.path.exists(json_dir):
        os.mkdir(json_dir)

    anno_files = os.listdir(anno_dir)

    for name in tqdm(anno_files):
        xml_path = anno_dir + name
        info = voc07xmlparser(xml_path)
        jsname = name.split('.')[0]
        with open(json_dir + jsname + '.json', 'w') as f:
            json.dump(info, f, ensure_ascii=False)

