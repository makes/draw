from PyQt4 import QtGui

class CreateCommand(QtGui.QUndoCommand):
    def __init__(self, item, scene, position, parent = None):
        super(CreateCommand, self).__init__(parent)
        self._ui_messages = UiMessages()
        self._item = item
        self._scene = scene
        self._position = position
        self.setText(self._ui_messages.create)

    def redo(self):
        self._scene.addItem(self._item)
        self._item.setPos(self._position)
        self._item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self._item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

    def undo(self):
        self._scene.removeItem(self._item)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self._ui_messages.translate_messages()

class UiMessages(object):
    def __init__(self):
        self.translate_messages()

    def translate_messages(self):
        self.create = QtGui.QApplication.translate(
            "CreateCommand",
            "Create",
            None,
            QtGui.QApplication.UnicodeUTF8)

