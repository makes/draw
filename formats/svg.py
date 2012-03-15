import drawing

from PyQt4 import QtGui

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

ENABLED = True
FILE_EXTENSIONS = ['.svg']
FILTER_STRING = "SVG (*.svg)"

def save(filename, canvas):
    svg = Element('svg')
    svg.set('version', '1.1')
    svg.set('xmlns', 'http://www.w3.org/2000/svg')
    svg.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')

    for item in canvas.document.items():
        if isinstance(item, QtGui.QGraphicsLineItem):
            line = SubElement(svg, 'line')
            line.set('x1', str(item.line().x1()))
            line.set('y1', str(item.line().y1()))
            line.set('x2', str(item.line().x2()))
            line.set('y2', str(item.line().y2()))
            line.set('style', 'stroke:black; stroke-width:2;')

    file = open(filename, 'w')
    file.write(prettify_xml(svg))
    file.close()

def load(filename, canvas):
    document = drawing.Document()

    for (event, element) in ElementTree.iterparse(filename):
        tag = strip_xml_namespace(element.tag)
        if tag == "line":
            document.addLine(float(element.attrib['x1']),
                             float(element.attrib['y1']),
                             float(element.attrib['x2']),
                             float(element.attrib['y2']))

    canvas.document = document

def prettify_xml(element):
    ugly_xml = ElementTree.tostring(element, 'utf-8')
    reparsed_xml = minidom.parseString(ugly_xml)
    return reparsed_xml.toprettyxml(indent="  ")

def strip_xml_namespace(tag):
    """ ElementTree formats tags as {ns}tagname.
        This function strips the namespace. """
    if '}' in tag:
        return tag.split('}')[1]

