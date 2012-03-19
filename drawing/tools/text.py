from PyQt4 import QtCore, QtGui

import drawing
from drawing.tools.options.text import ToolOptionsText
from drawing.tools.commands.create import CreateCommand

class Text(QtCore.QObject):
    DEFAULT_COLOR = "purple"
    
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
        font = QtGui.QFont("Helvetica", 48)
        font.setKerning(False)
        self._format.setFont(font)
        self._cursor = None
        self._options_widget = ToolOptionsText(initial_color)
        self._connect_slots()

    def _connect_slots(self):
        self._options_widget.color_changed.connect(self._set_color)

    def select(self, canvas):
        self._canvas = canvas
        canvas.document.installEventFilter(self)

    def deselect(self):
        if self._active:
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

    #def refresh(self, point):
    #    line = self._object.line()
    #    self._object.setLine(line.x1(), line.y1(), point.x(), point.y())

    def abort(self):
        if not self._active:
            return
        self._canvas.document.removeItem(self._object)
        self._active = False

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            self.activate(event.scenePos())
            return True
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.abort()
        return False

    def _set_color(self, color):
        pen = self._format.textOutline()
        pen.setColor(color)
        self._format.setTextOutline(pen)

    def get_options_widget(self):
        return self._options_widget

    options_widget = property(get_options_widget)

    @classmethod
    def get_name(self):
        return QtGui.QApplication.translate("Text",
                                            "Text",
                                            None,
                                            QtGui.QApplication.UnicodeUTF8)

