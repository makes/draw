import drawing

from PyQt4 import QtCore, QtGui

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

    for item in reversed(canvas.document.items()):
        if isinstance(item, QtGui.QGraphicsLineItem):
            _save_line(svg, item)
        elif isinstance(item, QtGui.QGraphicsRectItem):
            _save_rect(svg, item)
        elif isinstance(item, QtGui.QGraphicsEllipseItem):
            _save_ellipse(svg, item)
        elif isinstance(item, QtGui.QGraphicsTextItem):
            _save_text(svg, item)

    file = open(filename, 'w')
    file.write(prettify_xml(svg))
    file.close()

def _pen_to_svg_attrib(pen):
    attrib = {}
    attrib['stroke'] = get_rgb_string(pen.color())
    width = pen.widthF()
    if width == 0:
        width = 1.0
    attrib['stroke-width'] = str(width) + "px"
    return attrib

def _brush_to_svg_attrib(brush):
    attrib = {}
    attrib['fill'] = 'none'
    return attrib

def _save_line(parent, line):
    svg_line = SubElement(parent, 'line')
    svg_line.set('x1', str(line.line().x1() + line.scenePos().x()))
    svg_line.set('y1', str(line.line().y1() + line.scenePos().y()))
    svg_line.set('x2', str(line.line().x2() + line.scenePos().x()))
    svg_line.set('y2', str(line.line().y2() + line.scenePos().y()))
    svg_line.attrib.update(_pen_to_svg_attrib(line.pen()))
    return svg_line

def _save_rect(parent, rect):
    svg_rect = SubElement(parent, 'rect')
    svg_rect.set('x', str(rect.rect().x() + rect.scenePos().x()))
    svg_rect.set('y', str(rect.rect().y() + rect.scenePos().y()))
    svg_rect.set('width', str(rect.rect().width()))
    svg_rect.set('height', str(rect.rect().height()))
    svg_rect.attrib.update(_pen_to_svg_attrib(rect.pen()))
    svg_rect.attrib.update(_brush_to_svg_attrib(rect.brush()))
    return svg_rect

def _save_ellipse(parent, ellipse):
    svg_ellipse = SubElement(parent, 'ellipse')
    rx = ellipse.rect().width() / 2 + ellipse.scenePos().x()
    ry = ellipse.rect().height() / 2 + ellipse.scenePos().y()
    svg_ellipse.set('cx', str(ellipse.rect().x() + rx))
    svg_ellipse.set('cy', str(ellipse.rect().y() + ry))
    svg_ellipse.set('rx', str(rx))
    svg_ellipse.set('ry', str(ry))
    svg_ellipse.attrib.update(_pen_to_svg_attrib(ellipse.pen()))
    svg_ellipse.attrib.update(_brush_to_svg_attrib(ellipse.brush()))
    return svg_ellipse

def _save_text(parent, text):
    svg_text = SubElement(parent, 'text')
    char_format = text.textCursor().charFormat()
    content = str(text.document().toPlainText())
    metrics = QtGui.QFontMetrics(char_format.font())
    ypadding = (text.boundingRect().height() - float(metrics.height())) / 2
    xpadding = (text.boundingRect().width() - float(metrics.width(content))) / 2
    svg_text.set('x', str(text.x() + xpadding))
    svg_text.set('y', str(text.y() + metrics.ascent() + ypadding + 0.5))
    svg_text.set('font-family', str(char_format.fontFamily()))
    svg_text.set('font-size', str(char_format.fontPointSize()) + "pt")
    if char_format.font().kerning():
        svg_text.set('kerning', 'auto')
    stroke = _pen_to_svg_attrib(char_format.textOutline())
    fill = _brush_to_svg_attrib(char_format.foreground())
    svg_text.attrib.update(stroke)
    svg_text.attrib.update(fill)
    svg_text.text = content
    return svg_text

def load(filename, canvas):
    document = drawing.Document()

    for (event, element) in ElementTree.iterparse(filename):
        tag = strip_xml_namespace(element.tag)
        if tag == "line":
            document.addItem(_load_line(element))
        if tag == "rect":
            document.addItem(_load_rect(element))
        if tag == "ellipse":
            document.addItem(_load_ellipse(element))
        if tag == "text":
            _load_text(document, element)

    canvas.document = document

def _svg_attrib_to_pen(svg_attrib):
    pen = QtGui.QPen()
    if 'stroke' in svg_attrib:
        pen.setColor(get_qcolor(svg_attrib['stroke']))
    if 'stroke-width' in svg_attrib:
        width = svg_attrib['stroke-width'].replace('px', '')
        pen.setWidthF(float(width))
    return pen

def _svg_attrib_to_brush(svg_attrib):
    brush = QtGui.QBrush(QtCore.Qt.transparent)
    return brush

def _svg_attrib_to_font(svg_attrib):
    font = QtGui.QFont()
    font.setKerning(False)
    if 'font-family' in svg_attrib:
        font.setFamily(svg_attrib['font-family'])
    if 'font-size' in svg_attrib:
        size = svg_attrib['font-size'].replace('pt', '')
        font.setPointSizeF(float(size))
    if 'kerning' in svg_attrib:
        if svg_attrib['kerning'] == 'auto':
            font.setKerning(True)
    return font

def _load_line(svg_line):
    pen = _svg_attrib_to_pen(svg_line.attrib)
    line = QtGui.QGraphicsLineItem(float(svg_line.attrib['x1']),
                                   float(svg_line.attrib['y1']),
                                   float(svg_line.attrib['x2']),
                                   float(svg_line.attrib['y2']))
    line.setPen(pen)
    line.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
    line.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
    return line

def _load_rect(svg_rect):
    pen = _svg_attrib_to_pen(svg_rect.attrib)
    rect = QtGui.QGraphicsRectItem(float(svg_rect.attrib['x']),
                                   float(svg_rect.attrib['y']),
                                   float(svg_rect.attrib['width']),
                                   float(svg_rect.attrib['height']))
    rect.setPen(pen)
    rect.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
    rect.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
    return rect

def _load_ellipse(svg_ellipse):
    pen = _svg_attrib_to_pen(svg_ellipse.attrib)
    x = float(svg_ellipse.attrib['cx']) - float(svg_ellipse.attrib['rx'])
    y = float(svg_ellipse.attrib['cy']) - float(svg_ellipse.attrib['ry'])
    ellipse = QtGui.QGraphicsEllipseItem(x,
                                         y,
                                         float(svg_ellipse.attrib['rx']) * 2,
                                         float(svg_ellipse.attrib['ry']) * 2)
    ellipse.setPen(pen)
    ellipse.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
    ellipse.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
    return ellipse

def _load_text(document, svg_text):
    pen = _svg_attrib_to_pen(svg_text.attrib)
    brush = _svg_attrib_to_brush(svg_text.attrib)
    font = _svg_attrib_to_font(svg_text.attrib)
    content = svg_text.text.strip()
    textitem = QtGui.QGraphicsTextItem()
    charformat = QtGui.QTextCharFormat()
    charformat.setFont(font)
    charformat.setTextOutline(pen)
    charformat.setForeground(brush)
    cursor = QtGui.QTextCursor(textitem.document())
    cursor.setCharFormat(charformat)
    textitem.setTextCursor(cursor)
    cursor.insertText(content)
    metrics = QtGui.QFontMetrics(font)
    document.addItem(textitem)
    textitem.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
    textitem.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
    ypadding = (textitem.boundingRect().height()
                - float(metrics.height())) / 2
    xpadding = (textitem.boundingRect().width()
                - float(metrics.width(content))) / 2
    textitem.setX(float(svg_text.attrib['x']) - xpadding)
    textitem.setY(float(svg_text.attrib['y'])
                  - metrics.ascent()
                  - ypadding
                  - 0.5)

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

