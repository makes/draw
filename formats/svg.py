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
            pen = item.pen()
            color = get_rgb_string(pen.color())
            line = SubElement(svg, 'line')
            line.set('x1', str(item.line().x1()))
            line.set('y1', str(item.line().y1()))
            line.set('x2', str(item.line().x2()))
            line.set('y2', str(item.line().y2()))
            line.set('stroke-width', '1')
            line.set('stroke', color)

    file = open(filename, 'w')
    file.write(prettify_xml(svg))
    file.close()

def load(filename, canvas):
    document = drawing.Document()

    for (event, element) in ElementTree.iterparse(filename):
        tag = strip_xml_namespace(element.tag)
        if tag == "line":
            if 'stroke' in element.attrib:
                color = get_qcolor(element.attrib['stroke'])
            else:
                color = get_qcolor("")
            pen = QtGui.QPen(color)
            document.addLine(float(element.attrib['x1']),
                             float(element.attrib['y1']),
                             float(element.attrib['x2']),
                             float(element.attrib['y2']),
                             pen)

    canvas.document = document

def get_qcolor(rgb_string):
    if not rgb_string.lower().startswith('rgb('):
        return QtGui.QColor(0, 0, 0)
    comma_separated = rgb_string.split('(')[1].replace(')', '')
    values = comma_separated.split(',')
    return QtGui.QColor(int(values[0]),
                        int(values[1]),
                        int(values[2]))

def get_rgb_string(qcolor):
    return "rgb(%s,%s,%s)" % (str(qcolor.red()),
                              str(qcolor.green()),
                              str(qcolor.blue()))

def prettify_xml(element):
    ugly_xml = ElementTree.tostring(element, 'utf-8')
    reparsed_xml = minidom.parseString(ugly_xml)
    return reparsed_xml.toprettyxml(indent="  ")

def strip_xml_namespace(tag):
    """ ElementTree formats tags as {ns}tagname.
        This function strips the namespace. """
    if '}' in tag:
        return tag.split('}')[1]

