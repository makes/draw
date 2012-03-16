from PyQt4 import QtCore, QtGui

import drawing
from drawing.tools.options.rect import ToolOptionsRect
from drawing.tools.commands.create import CreateCommand

class Rect(QtCore.QObject):
    DEFAULT_COLOR = "blue"
    
    def __init__(self):
        super(Rect, self).__init__()
        self._canvas = None
        self._active = False
        self._object = None
        initial_color = QtGui.QColor(self.DEFAULT_COLOR)
        self._pen = QtGui.QPen(initial_color)
        self._options_widget = ToolOptionsRect(initial_color)
        self._connect_slots()

    def _connect_slots(self):
        self._options_widget.color_changed.connect(self._set_color)

    def select(self, canvas):
        self._canvas = canvas
        canvas.document.installEventFilter(self)

    def activate(self, point):
        if not self._active:  # First click - create new line
            self._active = True
            self._object = self._canvas.document.addRect(point.x(),
                                                         point.y(),
                                                         0,
                                                         0,
                                                         self._pen)
            self._qrect = self._object.rect()
            self._canvas.setMouseTracking(True)
        else:
            self._canvas.setMouseTracking(False)
            self.finalize()

    def finalize(self):
        self._active = False
        command = CreateCommand(self._object,
                                self._canvas.document,
                                self._object.pos())
        self._canvas.document.removeItem(self._object)
        self._canvas.execute(command)

    def refresh(self, point):
        rect = self._object.rect()
        self._qrect.setWidth(point.x() - self._qrect.x())
        self._qrect.setHeight(point.y() - self._qrect.y())
        self._object.setRect(self._qrect.normalized())

    def abort(self):
        if not self._active:
            return
        self._canvas.setMouseTracking(False)
        self._canvas.document.removeItem(self._object)
        self._active = False

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            self.activate(event.scenePos())
            return True
        elif event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            if self._active:
                self.refresh(event.scenePos())
            return True
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.abort()
        return False

    def _set_color(self, color):
        self._pen = QtGui.QPen(color)

    def get_options_widget(self):
        return self._options_widget

    options_widget = property(get_options_widget)

    @classmethod
    def get_name(self):
        return QtGui.QApplication.translate("Rect",
                                            "Rectangle",
                                            None,
                                            QtGui.QApplication.UnicodeUTF8)

