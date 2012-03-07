from PyQt4 import QtCore, QtGui
import functools
import inspect

from ui.draw_main_window import Ui_MainWindow

import drawing
import drawing.tools

class DrawMainWindow(QtGui.QMainWindow):
    DEFAULT_TOOL_CLASSNAME = "Pick"

    def __init__(self):
        self.ui_messages = UiMessages()
        self._new_count = 0

        # Get all drawing tools in module, instantiate and add to a dict.
        self._tools = {}
        for name, obj in inspect.getmembers(drawing.tools):
            if inspect.isclass(obj):
                self._tools[name] = obj()

        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connect_slots()
        self._init_interface()

    def _connect_slots(self):
        self.ui.actionNew.triggered.connect(self._handle_new)
        self.ui.actionSelectPickTool.triggered.connect(
            functools.partial(self.set_current_tool, self.get_tool("Pick")))
        self.ui.actionSelectPenTool.triggered.connect(
            functools.partial(self.set_current_tool, self.get_tool("Pen")))
        self.ui.menuWindow.aboutToShow.connect(self.update_window_menu)

    def _init_interface(self):
        self.show()

    def _handle_new(self):
        new_document = drawing.Document()
        new_canvas = drawing.Canvas(self.get_tool(self.DEFAULT_TOOL_CLASSNAME),
                                    new_document)
        new_window = self.ui.mdiArea.addSubWindow(new_canvas)
        self._new_count = self._new_count + 1
        new_window.setWindowTitle(self.ui_messages.default_doc_name
                                  + str(self._new_count))
        new_window.show()

    def get_tool(self, name):
        if name in self._tools:
            return self._tools[name]
        else:
            return None

    def set_current_tool(self, tool):
        self.ui.statusbar.clearMessage()
        canvas = self.get_active_canvas()
        if not canvas:
            self.ui.statusbar.showMessage(self.ui_messages.tool_unavailable,
                                          8000)
            return
        self.ui.statusbar.showMessage(self.ui_messages.selected_tool + ": "
                                      + tool.get_name(), 3000)
        canvas.set_current_tool(tool)

    def get_active_canvas(self):
        window = self.ui.mdiArea.activeSubWindow()
        if not window:
            return None
        return window.widget()

    def set_active_subwindow(self, window):
        self.ui.mdiArea.setActiveSubWindow(window)

    def update_window_menu(self):
        windows = self.ui.mdiArea.subWindowList()
        self.ui.menuWindow.clear()

        for window in windows:
            action = self.ui.menuWindow.addAction(window.windowTitle())
            action.setCheckable(True)
            action.setChecked(window == self.ui.mdiArea.activeSubWindow())
            action.triggered.connect(
                functools.partial(self.set_active_subwindow, window))

    def changeEvent(self, event):
        if type(event) == QtCore.QEvent.LanguageChange:
            self.ui.retranslateUi(self)
            self.ui_messages.translate_messages()

class UiMessages(object):
    def __init__(self):
        self.translate_messages()

    def translate_messages(self):
        self.tool_unavailable = QtGui.QApplication.translate("UiMessages",
            "You must open or create a drawing before activating these "
            "tools. Press Ctrl+N to create a new drawing.",
            None,
            QtGui.QApplication.UnicodeUTF8)

        self.default_doc_name = QtGui.QApplication.translate("UiMessages",
            "untitled-",
            None,
            QtGui.QApplication.UnicodeUTF8)

        self.selected_tool = QtGui.QApplication.translate("UiMessages",
            "Selected tool",
            None,
            QtGui.QApplication.UnicodeUTF8)

