from PyQt4 import QtCore, QtGui

from drawing.tools.options.pick import ToolOptionsPick
from drawing.tools.commands.move import MoveCommand
from drawing.tools.commands.delete import DeleteCommand

class Pick(QtCore.QObject):
    def __init__(self):
        super(Pick, self).__init__()
        self._canvas = None
        self._moving = False
        self._item_pos = QtCore.QPointF()
        self._options_widget = ToolOptionsPick()
        self._connect_slots()

    def _connect_slots(self):
        self._options_widget.color_changed.connect(self._set_color)

    def select(self, canvas):
        self._canvas = canvas
        self._canvas.document.selectionChanged.connect(self._update_color)
        canvas.document.installEventFilter(self)
        canvas.setCursor(self.get_cursor())

    def reset(self):
        if self._canvas:
            self._canvas.unsetCursor()
            self._canvas.document.clearSelection()

    def deactivate(self):
        pass

    def activate(self, point):
        item = self._canvas.document.itemAt(point)
        kbmod = QtGui.QApplication.keyboardModifiers()
        multi_select = (kbmod & QtCore.Qt.ControlModifier |
                        kbmod & QtCore.Qt.ShiftModifier)
        # Allow selection of multiple objects when Ctrl or
        # Shift is pressed.
        if not (multi_select):
            self._canvas.document.clearSelection()
        if item:
            if (item.flags() & QtGui.QGraphicsItem.ItemIsSelectable and
                item.isEnabled()):
                item.setSelected(True)
                if multi_select:
                    return True
                self._item_pos = item.scenePos()
        return False

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseDoubleClick:
            # Do nothing on double click.
            return True
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            return self.activate(event.scenePos())
        if event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            # Allow move by dragging only single item at a time.
            if len(self._canvas.document.selectedItems()) == 1:
                self._moving = True
                return False
            else:
                return True
        if event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            item = self._canvas.document.itemAt(event.scenePos())
            if item:
                if (item.flags() & QtGui.QGraphicsItem.ItemIsSelectable and
                    item.isEnabled()):
                    if self._moving:
                        command = MoveCommand(item,
                                              self._canvas.document,
                                              self._item_pos,
                                              item.scenePos())
                        self._canvas.execute(command)
                        self._moving = False
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Delete:
                selection = self._canvas.document.selectedItems()
                if len(selection) > 0:
                    command = DeleteCommand(selection, self._canvas.document)
                    self._canvas.execute(command)
            if event.key() == QtCore.Qt.Key_A:
                kbmod = QtGui.QApplication.keyboardModifiers()
                if kbmod & QtCore.Qt.ControlModifier:
                    # Ctrl-A pressed, select all
                    for item in self._canvas.document.items():
                        item.setSelected(True)
        return False

    def _get_item_color(self, item):
        if (isinstance(item, QtGui.QGraphicsLineItem) or
            isinstance(item, QtGui.QGraphicsRectItem) or
            isinstance(item, QtGui.QGraphicsEllipseItem)):
            return item.pen().color()
        if isinstance(item, QtGui.QGraphicsTextItem):
            return item.textCursor().charFormat().textOutline().color()

    def _set_item_color(self, item, color):
        if (isinstance(item, QtGui.QGraphicsLineItem) or
            isinstance(item, QtGui.QGraphicsRectItem) or
            isinstance(item, QtGui.QGraphicsEllipseItem)):
            pen = item.pen()
            pen.setColor(color)
            item.setPen(pen)
        if isinstance(item, QtGui.QGraphicsTextItem):
            # Manipulating TextItem's outline is ugly.
            # So many layers :(
            content = str(item.document().toPlainText())
            cursor = item.textCursor()
            charformat = cursor.charFormat()
            pen = charformat.textOutline()
            pen.setColor(color)
            charformat.setTextOutline(pen)
            for c in range(len(content)):
                cursor.deletePreviousChar()
            cursor.setCharFormat(charformat)
            item.setTextCursor(cursor)
            item.setTextCursor(cursor)
            cursor.insertText(content)

    def _update_color(self):
        selection = self._canvas.document.selectedItems()
        if len(selection) == 0:
            self._options_widget.set_color(QtGui.QColor("white"))
            self._options_widget.enable_color_selection(False)
        else:
            item = selection[0]
            color = self._get_item_color(item)
            self._options_widget.enable_color_selection(True)
            self._options_widget.set_color(color)

    def _set_color(self, color):
        selection = self._canvas.document.selectedItems()
        assert len(selection) > 0, "Can't set color if no object is selected."
        for item in selection:
            self._set_item_color(item, color)

    def get_options_widget(self):
        return self._options_widget

    @classmethod
    def get_name(self):
        return QtGui.QApplication.translate("Pick",
                                            "Pick",
                                            None,
                                            QtGui.QApplication.UnicodeUTF8)
    def get_cursor(self):
        xpm_map =  [ "32 32 2 1",
                     ". c #ffffff",
                     "O c #000000",
                     "................................",
                     "................................",
                     "................................",
                     "...O............................",
                     "...OO...........................",
                     "...OOO..........................",
                     "...OOOO.........................",
                     "...OOOOO........................",
                     "...OOOOOO.......................",
                     "...OOOOOOO......................",
                     "...OOOOOOOO.....................",
                     "...OOOOOOOOO....................",
                     "...OOOOOOOOOO...................",
                     "...OOOOOOOOOOO..................",
                     "...OOOOOOO......................",
                     "...OOOOOOO......................",
                     "...OOO.OOOO.....................",
                     "...O...OOOO.....................",
                     "........OOOO....................",
                     "........OOOO....................",
                     ".........OOOO...................",
                     ".........OOOO...................",
                     "..........OO....................",
                     "................................",
                     "................................",
                     "................................",
                     "................................",
                     "................................",
                     "................................",
                     "................................",
                     "................................",
                     "................................" ]

        xpm_mask = [ "32 32 2 1",
                     ". c #ffffff",
                     "O c #000000",
                     "................................",
                     "................................",
                     "..OO............................",
                     "..OOO...........................",
                     "..OOOO..........................",
                     "..OOOOO.........................",
                     "..OOOOOO........................",
                     "..OOOOOOO.......................",
                     "..OOOOOOOO......................",
                     "..OOOOOOOOO.....................",
                     "..OOOOOOOOOO....................",
                     "..OOOOOOOOOOO...................",
                     "..OOOOOOOOOOOO..................",
                     "..OOOOOOOOOOOOO.................",
                     "..OOOOOOOOOOOOO.................",
                     "..OOOOOOOOO.....................",
                     "..OOOOOOOOOO....................",
                     "..OOOOOOOOOO....................",
                     "..OO...OOOOOO...................",
                     ".......OOOOOO...................",
                     "........OOOOOO..................",
                     "........OOOOOO..................",
                     ".........OOOO...................",
                     "..........OO....................",
                     "................................",
                     "................................",
                     "................................",
                     "................................",
                     "................................",
                     "................................",
                     "................................",
                     "................................" ]

        pixmap = QtGui.QPixmap(xpm_map)
        mask = QtGui.QBitmap(QtGui.QPixmap(xpm_mask))
        pixmap.setMask(mask)
        return QtGui.QCursor(pixmap, 3, 3)

    options_widget = property(get_options_widget)

