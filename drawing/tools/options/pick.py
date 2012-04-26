from PyQt4 import QtCore, QtGui
from ui.tool_options_pick import Ui_ToolOptionsPick

class ToolOptionsPick(QtGui.QWidget):
    color_changed = QtCore.pyqtSignal(QtGui.QColor)

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_ToolOptionsPick()
        self.ui.setupUi(self)
        self.ui.colorSwatch.color = QtGui.QColor("white")
        self._connect_slots()

    def _connect_slots(self):
        self.ui.colorSwatch.color_changed.connect(self.color_selected)

    def color_selected(self, color):
        self.color_changed.emit(color)

    def set_color(self, color):
        self.ui.colorSwatch.set_color_no_event(color)

    def enable_color_selection(self, value):
        self.ui.colorSwatch.setEnabled(value)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.ui.retranslateUi(self)

