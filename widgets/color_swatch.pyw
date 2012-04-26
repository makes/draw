from PyQt4 import QtCore, QtGui

class ColorSwatch(QtGui.QFrame):
    color_changed = QtCore.pyqtSignal(QtGui.QColor)

    def __init__(self, parent = None):
        super(ColorSwatch, self).__init__(parent)
        self._ui_messages = UiMessages()
        self.setAutoFillBackground(True)
        self.set_color(QtGui.QColor("red"))

    def set_color(self, color):
        self.set_color_no_event(color)
        self.color_changed.emit(self._current_color)

    def set_color_no_event(self, color):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)
        self._current_color = color

    def get_color(self):
        return self._current_color

    def mousePressEvent(self, event):
        color = QtGui.QColorDialog.getColor(self._current_color,
                                            self,
                                            self._ui_messages.select_color)
        if color.isValid():
            self.set_color(color)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self._ui_messages.translate_messages()

    color = property(get_color, set_color)

class UiMessages(object):
    def __init__(self):
        self.translate_messages()

    def translate_messages(self):
        self.select_color = QtGui.QApplication.translate("ColorSwatch",
            "Select Color",
            None,
            QtGui.QApplication.UnicodeUTF8)

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    color = ColorSwatch()
    color.show()
    sys.exit(app.exec_())

