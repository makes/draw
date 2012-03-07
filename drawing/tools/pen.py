from PyQt4 import QtCore, QtGui

import drawing

class Pen(QtCore.QObject):
    def __init__(self):
        super(Pen, self).__init__()
        self._canvas = None
        self._active = False
        self._object = None

    def select(self, canvas):
        self._canvas = canvas
        canvas.document.installEventFilter(self)

    def activate(self, point):
        if not self._active:  # First click - create new line
            self._active = True
            self._object = self._canvas.document.addLine(point.x(),
                                                         point.y(),
                                                         point.x(),
                                                         point.y())
            self._canvas.setMouseTracking(True)
        else:
            self._active = False
            self._canvas.setMouseTracking(False)

    def refresh(self, point):
        line = self._object.line()
        self._object.setLine(line.x1(), line.y1(), point.x(), point.y())

    def abort(self):
        if not self._active:
            return
        self._canvas.setMouseTracking(False)
        self._canvas.document.removeItem(self._object)
        self._active = False

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            print "Mouse release: " + str(event.scenePos())
            self.activate(event.scenePos())
            return True
        elif event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            print "Mouse move: " + str(event.scenePos())
            if self._active:
                self.refresh(event.scenePos())
            return True
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.abort()
        print "caught event " + str(event.type())
        return False

    @classmethod
    def get_name(self):
        return QtGui.QApplication.translate("Pen",
                                            "Pen",
                                            None,
                                            QtGui.QApplication.UnicodeUTF8)

