#!/usr/bin/env python3
"""This script adds Trados-style attributes and elements in tmx files.

BEFORE RUNNING THIS SCRIPT:
<?xml version='1.0' encoding='UTF-8'?>
<tmx version="1.4">
  <header srclang="en-US" />
  <body>
    <tu>
      <tuv xml:lang="EN-US">
        <seg>The White House</seg>
      </tuv>
      <tuv xml:lang="RU-RU">
        <seg>Белый дом</seg>
      </tuv>
    </tu>
    <tu>
      <tuv xml:lang="EN-US">
        <seg>Office of the Press Secretary</seg>
      </tuv>
      <tuv xml:lang="RU-RU">
        <seg>Офис пресс-секретаря</seg>
      </tuv>
    </tu>
  </body>
</tmx>

AFTER RUNNING THIS SCRIPT:
<?xml version='1.0' encoding='UTF-8'?>
<tmx version="1.4">
  <header creationtool="SDL Language Platform" o-tmf="SDL TM8 Format" srclang="en-US">
    <prop type="x-Recognizers">RecognizeAll</prop>
    <prop type="x-filename:MultipleString" />
  </header>
  <body>
    <tu>
      <prop type="x-filename:MultipleString">some file name.tmx</prop>
      <tuv xml:lang="EN-US">
        <seg>The White House</seg>
      </tuv>
      <tuv xml:lang="RU-RU">
        <seg>Белый дом</seg>
      </tuv>
    </tu>
    <tu>
      <prop type="x-filename:MultipleString">some file name.tmx</prop>
      <tuv xml:lang="EN-US">
        <seg>Office of the Press Secretary</seg>
      </tuv>
      <tuv xml:lang="RU-RU">
        <seg>Офис пресс-секретаря</seg>
      </tuv>
    </tu>
  </body>
</tmx>
"""

import os
import argparse
import xml.etree.ElementTree as ET


def indent(elem, level=0):
    """Create indentation for tree elements."""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def get_tmx_file_contents(file_path):
    """Return tmx file contents."""
    with open(file_path, 'r', encoding='utf8') as inFile:
        contents = inFile.read()
    return contents


def add_tree_elements(tmx_contents_string, prop_text):
    """Return a modified ElementTree parsed from the tmx file content."""
    root = ET.fromstring(tmx_contents_string)

    header = root.find('header')
    header.set('creationtool', "SDL Language Platform")
    header.set('o-tmf', "SDL TM8 Format")

    header_attib_list = [subel.attrib for subel in header.iter()]
    header_attib_prop_values = []
    for d in header_attib_list:
        header_attib_prop_values.extend(list(d.values()))
    if 'x-Recognizers' not in header_attib_prop_values:
        prop = ET.SubElement(header, 'prop', attrib={'type': 'x-Recognizers'})
        prop.text = 'RecognizeAll'

    f_name_single_in = 'x-filename:SingleString' in header_attib_prop_values
    f_name_single_out = 'x-filename:SingleString' not in header_attib_prop_values
    f_name_multiple_in = 'x-filename:MultipleString' in header_attib_prop_values
    f_name_multiple_out = 'x-filename:MultipleString' not in header_attib_prop_values
    if f_name_single_in and f_name_multiple_out:
        prop = ET.SubElement(header, 'prop', attrib={'type': 'x-filename:MultipleString'})
        prop_to_remove = 'x-filename:SingleString'

        for prop in header.iter('prop'):
            if prop.get('type') == prop_to_remove:
                header.remove(prop)

        multi_el_prop = ET.Element('prop', attrib={'type': 'x-filename:MultipleString'})
        multi_el_prop.text = prop_text

        for tu in root.iter('tu'):
            for prop in tu.iter('prop'):
                if prop.get('type') == prop_to_remove:
                    tu.remove(prop)
            tu.insert(0, multi_el_prop)
    elif f_name_single_out and f_name_multiple_out:
        prop = ET.SubElement(header, 'prop', attrib={'type': 'x-filename:MultipleString'})
        prop = ET.Element('prop', attrib={'type': 'x-filename:MultipleString'})
        prop.text = prop_text
        for tu in root.iter('tu'):
            tu.insert(0, prop)
    elif f_name_single_out and f_name_multiple_in:
        # assume if filename is in header, it is also in <tu> 
        for tu in root.iter('tu'):
            for prop in tu.iter('prop'):
                if prop.get('type') == 'x-filename:MultipleString':
                    prop.text = prop_text
    indent(root)
    # return tree
    return ET.ElementTree(root)


def create_tmx(file1, file2):
    """Create a tmx file from two files."""
    tmx_contents = get_tmx_file_contents(file1)
    _, prop_text = os.path.split(file1)
    tree = add_tree_elements(tmx_contents, prop_text)

    tree.write(file2, encoding='UTF-8', xml_declaration=True)


def main():
    """Run the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path1',
                        help='Provide input file path')
    parser.add_argument('path2',
                        help='Provide output file path')
    args = parser.parse_args()

    file1 = args.path1
    file2 = args.path2
    create_tmx(file1, file2)


if __name__ == '__main__':
    main()
