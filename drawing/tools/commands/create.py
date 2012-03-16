from PyQt4 import QtGui

class CreateCommand(QtGui.QUndoCommand):
    def __init__(self, item, scene, position, parent = None):
        super(CreateCommand, self).__init__(parent)
        self._item = item
        self._scene = scene
        self._position = position

    def redo(self):
        self._scene.addItem(self._item)
        self._item.setPos(self._position)

    def undo(self):
        self._scene.removeItem(self._item)

