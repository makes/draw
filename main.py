import sys
from PyQt4 import QtCore, QtGui

from app import DrawApplication
#from language.lang import LanguageManager
from draw import DrawMainWindow

def main(*args):
    app = DrawApplication(sys.argv)

    # Set Qt plugin path manually (to help py2exe find them)
    qt_lib_paths = QtCore.QCoreApplication.libraryPaths()
    qt_lib_paths.append(QtCore.QCoreApplication.applicationDirPath() + "/plugins")
    QtCore.QCoreApplication.setLibraryPaths(qt_lib_paths)

    # Install translator
    lang = app.get_language_manager()
    lang.select("English")

    window = DrawMainWindow(lang)

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main(*sys.argv))
