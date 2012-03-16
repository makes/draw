from PyQt4 import QtGui, QtCore

class Document(QtGui.QGraphicsScene):
    dirty_changed = QtCore.pyqtSignal(bool)
    
    def __init__(self):
        super(Document, self).__init__()
        self._dirty = False

    def set_dirty(self, dirty):
        self._dirty = dirty
        self.dirty_changed.emit(self._dirty)

    def get_dirty(self):
        return self._dirty

    dirty = property(get_dirty, set_dirty)

