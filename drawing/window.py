from PyQt4 import QtGui, QtCore

import drawing

class Window(QtGui.QMdiSubWindow):
    window_closed = QtCore.pyqtSignal(QtGui.QMdiSubWindow)

    def __init__(self, main, parent, canvas):
        super(Window, self).__init__(parent)
        self.setWidget(canvas)
        self._canvas = canvas
        self._main = main

    def closeEvent(self, event):
        if not self.get_dirty():
            event.accept()
            self.window_closed.emit(self)
            return
        confirm_dialog = QtGui.QMessageBox(QtGui.QMessageBox.Question,
                                           "Unsaved Changes",
                                           "The drawing has been modified.",
                                           QtGui.QMessageBox.Save |
                                           QtGui.QMessageBox.Discard |
                                           QtGui.QMessageBox.Cancel,
                                           self)
        confirm_dialog.setInformativeText("Do you want to save your changes?")
        confirm_dialog.setDefaultButton(QtGui.QMessageBox.Save)
        dialog_result = confirm_dialog.exec_()
        if dialog_result == QtGui.QMessageBox.Save:
            save_result = self._main.save()
            if save_result:
                event.accept()
            else:
                event.ignore()
                return
        elif dialog_result == QtGui.QMessageBox.Discard:
            event.accept()
        elif dialog_result == QtGui.QMessageBox.Cancel:
            event.ignore()
            return
        self.window_closed.emit(self)

    def get_canvas(self):
        return self._canvas

    def set_canvas(self, canvas):
        self._canvas = canvas

    def get_filename(self):
        return self._canvas.filename

    def set_filename(self, filename):
        self.setWindowTitle(filename)
        self._canvas.filename = filename

    def get_dirty(self):  # fuck yea
        return self.canvas.get_dirty()

    canvas = property(get_canvas, set_canvas)
    filename = property(get_filename, set_filename)

