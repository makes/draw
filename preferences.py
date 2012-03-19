from PyQt4 import QtGui

from ui.preferences_dialog import Ui_PreferencesDialog

class PreferencesDialog(QtGui.QDialog):
    def __init__(self, parent, languages, cur_lang_idx):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self.ui.languageDropdown.insertItems(0, languages)
        self.ui.languageDropdown.setCurrentIndex(cur_lang_idx)
        self._connect_slots()

    def _connect_slots(self):
        self.ui.btnOK.clicked.connect(self.accept)
        self.ui.btnCancel.clicked.connect(self.reject)

    def get_language(self):
        return str(self.ui.languageDropdown.currentText())

