from PyQt4 import QtCore, QtGui
from ui.tool_options_text import Ui_ToolOptionsText

class ToolOptionsText(QtGui.QWidget):
    color_changed = QtCore.pyqtSignal(QtGui.QColor)
    font_size_changed = QtCore.pyqtSignal(int)

    def __init__(self, color):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_ToolOptionsText()
        self.ui.setupUi(self)
        self.ui.colorSwatch.color = color
        self.ui.cboFontSize.addItem("6")
        self.ui.cboFontSize.addItem("7")
        self.ui.cboFontSize.addItem("8")
        self.ui.cboFontSize.addItem("9")
        self.ui.cboFontSize.addItem("10")
        self.ui.cboFontSize.addItem("11")
        self.ui.cboFontSize.addItem("12")
        self.ui.cboFontSize.addItem("14")
        self.ui.cboFontSize.addItem("16")
        self.ui.cboFontSize.addItem("18")
        self.ui.cboFontSize.addItem("24")
        self.ui.cboFontSize.addItem("36")
        self.ui.cboFontSize.addItem("48")
        self.ui.cboFontSize.addItem("64")
        self.ui.cboFontSize.addItem("72")
        self.ui.cboFontSize.addItem("100")
        self.ui.cboFontSize.addItem("150")
        self.ui.cboFontSize.addItem("200")
        self.ui.cboFontSize.setCurrentIndex(12)
        self._connect_slots()

    def _connect_slots(self):
        self.ui.colorSwatch.color_changed.connect(self.color_selected)
        self.ui.cboFontSize.currentIndexChanged.connect(self.font_size_selected)

    def color_selected(self, color):
        self.color_changed.emit(color)

    def font_size_selected(self, index):
        size_string = self.ui.cboFontSize.itemText(index)
        self.font_size_changed.emit(int(size_string))

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.ui.retranslateUi(self)

