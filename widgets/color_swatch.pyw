from PyQt4 import QtCore, QtGui

class ColorSwatch(QtGui.QFrame):
    color_changed = QtCore.pyqtSignal(QtGui.QColor)

    def __init__(self, parent = None):
        super(ColorSwatch, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.set_color(QtGui.QColor("red"))

    def set_color(self, color):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)
        self._current_color = color
        self.color_changed.emit(self._current_color)

    def get_color(self):
        return self._current_color

    def mousePressEvent(self, event):
        color = QtGui.QColorDialog.getColor(self._current_color,
                                            self,
                                            "Select Color")
        self.set_color(color)

    color = property(get_color, set_color)

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    color = ColorSwatch()
    color.show()
    sys.exit(app.exec_())

