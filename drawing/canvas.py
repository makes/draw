from PyQt4 import QtGui, QtCore

import drawing
import drawing.tools

class Canvas(QtGui.QGraphicsView):
    dirty_changed = QtCore.pyqtSignal(bool)
    
    def __init__(self, default_tool, document):
        super(Canvas, self).__init__(document)
        self._current_tool = None
        self.set_current_tool(default_tool)
        self._undo_stack = QtGui.QUndoStack(self)
        self._filename = None
        document.dirty_changed.connect(self.forward_dirty_changed)

    def get_current_tool(self):
        return self._current_tool

    def set_current_tool(self, tool):
        if self._current_tool:
            self.document.removeEventFilter(self._current_tool)
        self._current_tool = tool
        tool.select(self)

    def execute(self, command):
        self._undo_stack.push(command)
        self.set_dirty(True)

    def get_undo_stack(self):
        return self._undo_stack

    def get_document(self):
        return self.scene()

    def set_document(self, document):
        self.setScene(document)

    def set_filename(self, filename):
        self._filename = filename

    def get_filename(self):
        return self._filename

    def forward_dirty_changed(self, dirty):
        self.dirty_changed.emit(dirty)

    def set_dirty(self, dirty):
        self.document.dirty = dirty

    def get_dirty(self):
        return self.document.get_dirty()

    document = property(get_document, set_document)
    tool = property(get_current_tool, set_current_tool)
    undo_stack = property(get_undo_stack)
    filename = property(get_filename, set_filename)

