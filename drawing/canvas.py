from PyQt4 import QtGui

import drawing
import drawing.tools

class Canvas(QtGui.QGraphicsView):
    def __init__(self, default_tool, document):
        super(Canvas, self).__init__(document)
        self._current_tool = None
        self.set_current_tool(default_tool)

    def get_current_tool(self):
        return self._current_tool

    def set_current_tool(self, tool):
        if self._current_tool:
            self.document.removeEventFilter(self._current_tool)
        self._current_tool = tool
        tool.select(self)

    def get_document(self):
        return self.scene()

    def set_document(self, document):
        self.setScene(document)

    document = property(get_document, set_document)
    tool = property(get_current_tool, set_current_tool)

