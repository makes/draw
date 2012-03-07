import sys
from PyQt4 import QtCore, QtGui

from draw import DrawMainWindow

def main(*args):
    app = QtGui.QApplication(sys.argv)

    # Set Qt plugin path manually (to help py2exe find them)
    qt_lib_paths = QtCore.QCoreApplication.libraryPaths()
    qt_lib_paths.append(QtCore.QCoreApplication.applicationDirPath() + "/plugins")
    QtCore.QCoreApplication.setLibraryPaths(qt_lib_paths)

    # Install translator
    translator = QtCore.QTranslator(app)
    translator.load("fi.qm")
    app.installTranslator(translator)

    window = DrawMainWindow()

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main(*sys.argv))
