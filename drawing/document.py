from PyQt4 import QtGui

class Document(QtGui.QGraphicsScene):
    def __init__(self):
        super(Document, self).__init__()
        self._dirty = False

    def set_dirty(self, dirty):
        self._dirty = dirty

    def get_dirty(self):
        return self._dirty

    dirty = property(get_dirty, set_dirty)

