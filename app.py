from PyQt4 import QtGui

from language.lang import LanguageManager

class DrawApplication(QtGui.QApplication):
    def __init__(self, args):
        super(DrawApplication, self).__init__(args)
        self._lang = LanguageManager()
        self._connect_slots()

    def _connect_slots(self):
        self._lang.language_selected.connect(self.set_translator)

    def get_language_manager(self):
        return self._lang

    def set_translator(self, translator):
        self.installTranslator(translator)

