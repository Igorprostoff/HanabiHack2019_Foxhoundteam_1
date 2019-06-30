# https://python-scripts.com/xml-python

import xml.etree.ElementTree as ET
import time

def parseXML(tag, filename):

    tree = ET.ElementTree(file=filename)
    root = tree.getroot()
    
    for begin_time in root.iter(tag):
        if begin_time.tag == tag:
            return begin_time.text
        else:
            print("ParseXML Error!")
 
def editXML(tag, tag_text, filename):

    tree = ET.ElementTree(file=filename)
    root = tree.getroot()
    
    for begin_time in root.iter(tag):
        begin_time.text = tag_text
    
    tree = ET.ElementTree(root)
    tree.write(filename)

def createXML(filename):

    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")

    begin = ET.SubElement(doc, "conf_file_id").text = "0"
    begin = ET.SubElement(doc, "all_files_number").text = "0"
    begin = ET.SubElement(doc, "isok_test").text = "ISOK"

    tree = ET.ElementTree(root)
    tree.write(filename)

def addXML(tag, tag_text, filename, index):
    
    root = ET.parse(filename).getroot()
    elem = ET.Element(tag)
    elem.text = tag_text
    root.insert(index, elem)
    #ET.dump(root)
    tree = ET.ElementTree(root)
    tree.write(filename)
    
    

if __name__ == "__main__":
    x = True
    createXML("test_config.xml")
    while x == True:
        print("Write tag: ")
        tag = str(input())
        print("Write tag_text: ")
        tag_text = str(input())
        filename = "test_config.xml"
        editXML(tag, tag_text, filename)
        print(parseXML(tag, filename))