from PyQt4 import QtGui, QtCore

import drawing
import drawing.tools

class Canvas(QtGui.QGraphicsView):
    clean_changed = QtCore.pyqtSignal(bool)
    
    def __init__(self, default_tool, document):
        super(Canvas, self).__init__(document)
        self._current_tool = None
        self.set_current_tool(default_tool)
        self._filename = None
        self._undo_stack = QtGui.QUndoStack(self)
        self._undo_stack.setUndoLimit(1000)
        self._undo_stack.cleanChanged.connect(self.clean_changed)

    def get_current_tool(self):
        return self._current_tool

    def set_current_tool(self, tool):
        if self._current_tool:
            self.document.removeEventFilter(self._current_tool)
        self._current_tool = tool
        tool.select(self)

    def execute(self, command):
        self._undo_stack.push(command)

    def get_document(self):
        return self.scene()

    def set_document(self, document):
        self.setScene(document)

    def set_filename(self, filename):
        self._filename = filename

    def get_filename(self):
        return self._filename

    def set_clean(self):
        self._undo_stack.setClean()

    def is_clean(self):
        return self._undo_stack.isClean()

    def get_undo_stack(self):
        return self._undo_stack

    document = property(get_document, set_document)
    tool = property(get_current_tool, set_current_tool)
    filename = property(get_filename, set_filename)

