import os
from glob import glob

from PyQt4 import QtCore

class LanguageManager(QtCore.QObject):
    language_selected = QtCore.pyqtSignal(QtCore.QTranslator)
    
    def __init__(self):
        super(LanguageManager, self).__init__()
        self._languages = {}
        for file in glob("./language/*.qm"):
            translator = QtCore.QTranslator()
            lang_name = os.path.basename(file).replace('.qm', '')
            translator.load(file)
            self._languages[lang_name] = translator

    def get_languages(self):
        return self._languages.keys()

    def get_current_language(self):
        return self._current_lang

    def get_current_language_index(self):
        return self._languages.keys().index(self._current_lang)

    def select(self, language):
        if language not in self._languages.keys():
            return
        self._current_lang = language
        self.language_selected.emit(self._languages[language])

    languages = property(get_languages)

if __name__ == "__main__":
    lang = Language(QtCore.QTranslator())
    print lang.get_languages()

