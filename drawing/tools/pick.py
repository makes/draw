from PyQt4 import QtCore, QtGui

class Pick(QtCore.QObject):
    def __init__(self):
        super(Pick, self).__init__()
        self._canvas = None

    def select(self, canvas):
        self._canvas = canvas
        canvas.document.installEventFilter(self)

    def deselect(self):
        pass

    def activate(self, point):
        pass

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            print "Mouse press: " + str(event.scenePos())
            self.activate(event.scenePos())
            return True
        return False

    def get_options_widget(self):
        return None

    @classmethod
    def get_name(self):
        return QtGui.QApplication.translate("Pick",
                                            "Pick",
                                            None,
                                            QtGui.QApplication.UnicodeUTF8)

    options_widget = property(get_options_widget)

