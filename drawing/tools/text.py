from PyQt4 import QtCore, QtGui

import drawing
from drawing.tools.options.text import ToolOptionsText
from drawing.tools.commands.create import CreateCommand

class Text(QtCore.QObject):
    DEFAULT_COLOR = "purple"
    DEFAULT_FONT_SIZE = 48

    def __init__(self):
        super(Text, self).__init__()
        self._canvas = None
        self._active = False
        self._object = None
        initial_color = QtGui.QColor(self.DEFAULT_COLOR)
        pen = QtGui.QPen(initial_color)
        pen.setWidthF(3.0)
        self._format = QtGui.QTextCharFormat()
        self._format.setTextOutline(pen)
        brush = QtGui.QBrush(QtCore.Qt.transparent)
        self._format.setForeground(brush)
        font = QtGui.QFont("Helvetica", self.DEFAULT_FONT_SIZE)
        font.setKerning(False)
        self._format.setFont(font)
        self._cursor = None
        self._options_widget = ToolOptionsText(initial_color)
        self._connect_slots()

    def _connect_slots(self):
        self._options_widget.color_changed.connect(self._set_color)
        self._options_widget.font_size_changed.connect(self._set_font_size)

    def select(self, canvas):
        self._canvas = canvas
        canvas.document.installEventFilter(self)
        canvas.setCursor(self.get_cursor())

    def reset(self):
        self.deactivate()
        if self._canvas:
            self._canvas.unsetCursor()

    def deactivate(self):
        self.finalize()

    def activate(self, point):
        if self._active:
            self.finalize()
        self._active = True
        self._object = QtGui.QGraphicsTextItem()
        self._object.setTextInteractionFlags(QtCore.Qt.TextEditable)
        self._cursor = QtGui.QTextCursor(self._object.document())
        self._cursor.setCharFormat(self._format)
        self._object.setTextCursor(self._cursor)
        self._canvas.document.addItem(self._object)
        self._object.document().contentsChanged.connect(self.fix_cursor)
        self._object.setX(point.x())
        self._object.setY(point.y())
        self._object.setFocus()

    def fix_cursor(self):
        if self._object.document().isEmpty():
            self._cursor = QtGui.QTextCursor(self._object.document())
            self._cursor.setCharFormat(self._format)
            self._object.setTextCursor(self._cursor)

    def finalize(self):
        if not self._active:
            return
        if self._object.document().isEmpty():
            self.abort()
            return
        self._active = False
        self._object.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        command = CreateCommand(self._object,
                                self._canvas.document,
                                self._object.pos())
        self._canvas.document.removeItem(self._object)
        self._canvas.execute(command)

    def abort(self):
        if not self._active:
            return
        self._canvas.document.removeItem(self._object)
        self._active = False

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseDoubleClick:
            # Do nothing on double click.
            return True
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            return True
        if event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            self.activate(event.scenePos())
            return True
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.abort()
        return False

    def _set_color(self, color):
        pen = self._format.textOutline()
        pen.setColor(color)
        self._format.setTextOutline(pen)

    def _set_font_size(self, font_size):
        font = self._format.font()
        font.setPointSize(font_size)
        self._format.setFont(font)

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
                     "...........O...........O........",
                     "......................OO........",
                     "......................OOO.......",
                     ".....................O.OO.......",
                     ".....................O..OO......",
                     ".....................O..OO......",
                     "....................O....OO.....",
                     "....................OOOOOOO.....",
                     "....................O....OOO....",
                     "...................O......OO....",
                     "..................OOOO...OOOO...",
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
                     "...........O...........O........",
                     "......................OO........",
                     "......................OOO.......",
                     ".....................O.OO.......",
                     ".....................O..OO......",
                     ".....................O..OO......",
                     "....................O....OO.....",
                     "....................OOOOOOO.....",
                     "....................O....OOO....",
                     "...................O......OO....",
                     "..................OOOO...OOOO...",
                     "................................",
                     "................................" ]

        pixmap = QtGui.QPixmap(xpm_map)
        mask = QtGui.QBitmap(QtGui.QPixmap(xpm_mask))
        pixmap.setMask(mask)
        return QtGui.QCursor(pixmap, 11, 11)

    options_widget = property(get_options_widget)

    @classmethod
    def get_name(self):
        return QtGui.QApplication.translate("Text",
                                            "Text",
                                            None,
                                            QtGui.QApplication.UnicodeUTF8)

