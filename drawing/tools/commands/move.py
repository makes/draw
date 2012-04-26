from PyQt4 import QtGui

class MoveCommand(QtGui.QUndoCommand):
    def __init__(self, item, scene, old_pos, new_pos, parent = None):
        super(MoveCommand, self).__init__(parent)
        self._ui_messages = UiMessages()
        self._item = item
        self._scene = scene
        self._old_pos = old_pos
        self._new_pos = new_pos
        self.setText(self._ui_messages.move)

    def redo(self):
        self._scene.clearSelection()
        self._item.setPos(self._new_pos)
        self._item.setSelected(True)

    def undo(self):
        self._scene.clearSelection()
        self._item.setPos(self._old_pos)
        self._item.setSelected(True)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self._ui_messages.translate_messages()

class UiMessages(object):
    def __init__(self):
        self.translate_messages()

    def translate_messages(self):
        self.move = QtGui.QApplication.translate(
            "MoveCommand",
            "Move",
            None,
            QtGui.QApplication.UnicodeUTF8)

