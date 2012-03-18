from PyQt4 import QtCore, QtGui
from ui.tool_options_ellipse import Ui_ToolOptionsEllipse

class ToolOptionsEllipse(QtGui.QWidget):
    color_changed = QtCore.pyqtSignal(QtGui.QColor)

    def __init__(self, color):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_ToolOptionsEllipse()
        self.ui.setupUi(self)
        self.ui.colorSwatch.color = color
        self._connect_slots()

    def _connect_slots(self):
        self.ui.colorSwatch.color_changed.connect(self.color_selected)

    def color_selected(self, color):
        self.color_changed.emit(color)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.ui.retranslateUi(self)

