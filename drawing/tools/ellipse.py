from PyQt4 import QtCore, QtGui

import drawing
from drawing.tools.options.ellipse import ToolOptionsEllipse
from drawing.tools.commands.create import CreateCommand

class Ellipse(QtCore.QObject):
    DEFAULT_COLOR = "red"
    
    def __init__(self):
        super(Ellipse, self).__init__()
        self._canvas = None
        self._active = False
        self._object = None
        initial_color = QtGui.QColor(self.DEFAULT_COLOR)
        self._pen = QtGui.QPen(initial_color)
        self._pen.setWidthF(3.0)
        self._options_widget = ToolOptionsEllipse(initial_color)
        self._connect_slots()

    def _connect_slots(self):
        self._options_widget.color_changed.connect(self._set_color)

    def select(self, canvas):
        self._canvas = canvas
        canvas.document.installEventFilter(self)
        canvas.setCursor(self.get_cursor())

    def reset(self):
        self.deactivate()
        if self._canvas:
            self._canvas.unsetCursor()

    def deactivate(self):
        self.abort()

    def activate(self, point):
        self._canvas.setViewportUpdateMode(
            QtGui.QGraphicsView.FullViewportUpdate)
        if not self._active:  # First click - create new ellipse
            self._active = True
            self._object = self._canvas.document.addEllipse(point.x(),
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
        if not self._active:
            return
        self._active = False
        command = CreateCommand(self._object,
                                self._canvas.document,
                                self._object.pos())
        self._canvas.document.removeItem(self._object)
        self._canvas.execute(command)
        self._canvas.setViewportUpdateMode(
            QtGui.QGraphicsView.MinimalViewportUpdate)

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
        self._canvas.setViewportUpdateMode(
            QtGui.QGraphicsView.MinimalViewportUpdate)
        self._active = False

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseDoubleClick:
            return True
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            return True
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
        self._pen.setColor(color)

    def get_options_widget(self):
        return self._options_widget

    def get_cursor(self):
        xpm_map =  [ "32 32 2 1",
                     ". c #ffffff",
                     "O c #000000",
                     "................................",
                     "................................",
                     "................................",
                     "...........O....................",
                     "................................",
                     "...........O....................",
                     "................................",
                     "...........O....................",
                     "................................",
                     "...........O....................",
                     "................................",
                     "...O.O.O.O...O.O.O.O............",
                     "................................",
                     "...........O....................",
                     "................................",
                     "...........O....................",
                     "................................",
                     "...........O....................",
                     "................................",
                     "...........O.........OOOOOO.....",
                     "...................OO......OO...",
                     "..................O..........O..",
                     ".................O............O.",
                     ".................O............O.",
                     ".................O............O.",
                     ".................O............O.",
                     "..................O..........O..",
                     "...................OO......OO...",
                     ".....................OOOOOO.....",
                     "................................",
                     "................................",
                     "................................" ]

        xpm_mask = [ "32 32 2 1",
                     ". c #ffffff",
                     "O c #000000",
                     "................................",
                     "................................",
                     "................................",
                     "...........O....................",
                     "...........O....................",
                     "...........O....................",
                     "...........O....................",
                     "...........O....................",
                     "...........O....................",
                     "...........O....................",
                     "................................",
                     "...OOOOOOO...OOOOOOO............",
                     "................................",
                     "...........O....................",
                     "...........O....................",
                     "...........O....................",
                     "...........O....................",
                     "...........O....................",
                     "...........O....................",
                     "...........O.........OOOOOO.....",
                     "...................OO......OO...",
                     "..................O..........O..",
                     ".................O............O.",
                     ".................O............O.",
                     ".................O............O.",
                     ".................O............O.",
                     "..................O..........O..",
                     "...................OO......OO...",
                     ".....................OOOOOO.....",
                     "................................",
                     "................................",
                     "................................" ]

        pixmap = QtGui.QPixmap(xpm_map)
        mask = QtGui.QBitmap(QtGui.QPixmap(xpm_mask))
        pixmap.setMask(mask)
        return QtGui.QCursor(pixmap, 11, 11)

    options_widget = property(get_options_widget)

    @classmethod
    def get_name(self):
        return QtGui.QApplication.translate("Ellipse",
                                            "Ellipse",
                                            None,
                                            QtGui.QApplication.UnicodeUTF8)

