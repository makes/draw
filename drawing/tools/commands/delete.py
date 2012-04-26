from PyQt4 import QtGui

class DeleteCommand(QtGui.QUndoCommand):
    def __init__(self, items, scene, parent = None):
        super(DeleteCommand, self).__init__(parent)
        self._ui_messages = UiMessages()
        self._items = {}
        self._scene = scene
        # Store items to delete and their positions in a dict
        for item in items:
            self._items[item] = item.scenePos()
        self.setText(self._ui_messages.delete)

    def redo(self):
        for item in self._items.keys():
            self._scene.removeItem(item)

    def undo(self):
        for item in self._items.keys():
            self._scene.addItem(item)
            item.setPos(self._items[item])
            item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
            item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self._scene.clearSelection()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self._ui_messages.translate_messages()

class UiMessages(object):
    def __init__(self):
        self.translate_messages()

    def translate_messages(self):
        self.delete = QtGui.QApplication.translate(
            "DeleteCommand",
            "Delete",
            None,
            QtGui.QApplication.UnicodeUTF8)

