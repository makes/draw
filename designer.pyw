# This is for firing up Qt Designer so that custom widgets are listed.

import sys
import os

from PyQt4 import QtCore, QtGui

app = QtGui.QApplication(sys.argv)

env = os.environ.copy()
env['PYQTDESIGNERPATH'] = 'widgets/designer'
env['PYTHONPATH'] = 'widgets'
qenv = ['%s=%s' % (name, value) for name, value in env.items()]

designer = QtCore.QProcess()
designer.setEnvironment(qenv)

designer_bin = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath)

if sys.platform == 'darwin':
    designer_bin += '/Designer.app/Contents/MacOS/Designer'
else:
    designer_bin += '/designer'

designer.start(designer_bin)
designer.waitForFinished(-1)

sys.exit(designer.exitCode())

