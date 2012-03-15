from PyQt4 import QtGui, QtDesigner
from color_swatch import ColorSwatch

class ColorSwatchPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent = None):
        super(ColorSwatchPlugin, self).__init__(parent)
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return ColorSwatch(parent)

    def name(self):
        return "ColorSwatch"

    def group(self):
        return "Drawing App"

    def icon(self):
        return None

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def domXml(self):
        return '<widget class="ColorSwatch" name="colorSwatch">\n' \
               '</widget>\n'

    def includeFile(self):
        return "widgets.color_swatch"

