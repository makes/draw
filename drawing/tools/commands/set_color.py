from PyQt4 import QtGui

class SetColorCommand(QtGui.QUndoCommand):
    def __init__(self, item, scene, old_color, new_color, parent = None):
        super(SetColorCommand, self).__init__(parent)
        self._ui_messages = UiMessages()
        self._item = item
        self._scene = scene
        self._old_color = old_color
        self._new_color = new_color
        self.setText(self._ui_messages.set_color)

    def redo(self):
        self._set_item_color(self._item, self._new_color)

    def undo(self):
        self._set_item_color(self._item, self._old_color)

    def _set_item_color(self, item, color):
        if (isinstance(item, QtGui.QGraphicsLineItem) or
            isinstance(item, QtGui.QGraphicsRectItem) or
            isinstance(item, QtGui.QGraphicsEllipseItem)):
            pen = item.pen()
            pen.setColor(color)
            item.setPen(pen)
        if isinstance(item, QtGui.QGraphicsTextItem):
            # Manipulating TextItem's outline is ugly.
            # So many layers :(
            content = str(item.document().toPlainText())
            cursor = item.textCursor()
            charformat = cursor.charFormat()
            pen = charformat.textOutline()
            pen.setColor(color)
            charformat.setTextOutline(pen)
            for c in range(len(content)):
                cursor.deletePreviousChar()
            cursor.setCharFormat(charformat)
            item.setTextCursor(cursor)
            item.setTextCursor(cursor)
            cursor.insertText(content)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self._ui_messages.translate_messages()

class UiMessages(object):
    def __init__(self):
        self.translate_messages()

    def translate_messages(self):
        self.set_color = QtGui.QApplication.translate(
            "SetColorCommand",
            "Set Color",
            None,
            QtGui.QApplication.UnicodeUTF8)

