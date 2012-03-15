import drawing

from PyQt4 import QtGui

from libs import pysvg
from libs.pysvg import parser as pysvg_parser
from libs.pysvg import builders as pysvg_builders

# This module is disabled, as the school assignment does not allow the use of
# an external SVG library.
ENABLED = False
FILE_EXTENSIONS = ['.svg']
FILTER_STRING = "SVG (*.svg)"

def save(filename, canvas):
    svg = pysvg.structure.svg()
    shb = pysvg_builders.ShapeBuilder()

    for item in canvas.document.items():
        if isinstance(item, QtGui.QGraphicsLineItem):
            line = shb.createLine(item.line().x1(),
                                  item.line().y1(),
                                  item.line().x2(),
                                  item.line().y2(),
                                  strokewidth = 2,
                                  stroke='black')
            #line = pysvg.shape.line(item.line().x1(),
            #                        item.line().y1(),
            #                        item.line().x2(),
            #                        item.line().y2())
            svg.addElement(line)

    svg.save(filename)

def load(filename, canvas):
    document = drawing.Document()
    svg = pysvg_parser.parse(filename)

    for line in svg.getElementsByType(pysvg.shape.line):
        document.addLine(float(line.get_x1()),
                         float(line.get_y1()),
                         float(line.get_x2()),
                         float(line.get_y2()))

    canvas.document = document

