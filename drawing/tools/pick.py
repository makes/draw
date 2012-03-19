from PyQt4 import QtCore, QtGui

class Pick(QtCore.QObject):
    def __init__(self):
        super(Pick, self).__init__()
        self._canvas = None

    def select(self, canvas):
        self._canvas = canvas
        canvas.document.installEventFilter(self)
        canvas.setCursor(self.get_cursor())

    def reset(self):
        if self._canvas:
            self._canvas.unsetCursor()

    def deactivate(self):
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

