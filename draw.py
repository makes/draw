from PyQt4 import QtCore, QtGui
import os.path
import functools
import inspect
import pkgutil

from ui.draw_main_window import Ui_MainWindow

import drawing
import drawing.tools

import formats

class DrawMainWindow(QtGui.QMainWindow):
    DEFAULT_TOOL_CLASSNAME = "Pick"
    DEFAULT_FORMAT_MODULENAME = "svg"

    def __init__(self):
        self.ui_messages = UiMessages()
        self._new_count = 0

        # Get all drawing tools in module, instantiate and add to a dict.
        self._tools = {}
        for name, obj in inspect.getmembers(drawing.tools):
            if inspect.isclass(obj):
                self._tools[name] = obj()

        # Load all file format modules in the 'formats' package.
        formats_path = os.path.dirname(formats.__file__)
        self._formats = {}
        for importer, modname, _ in pkgutil.iter_modules([formats_path]):
            full_modname = 'formats.%s' % modname
            module = importer.find_module(modname).load_module(full_modname)
            self._formats[modname] = module

        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connect_slots()
        self._init_interface()

    def _connect_slots(self):
        self.ui.actionNew.triggered.connect(self._handle_new)
        self.ui.actionSave.triggered.connect(self._handle_save)
        self.ui.actionSaveAs.triggered.connect(self._handle_save_as)
        self.ui.actionOpen.triggered.connect(self._handle_open)

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
        new_canvas.setSceneRect(0, 0, 10000, 10000)
        new_window = self.ui.mdiArea.addSubWindow(new_canvas)
        self._new_count = self._new_count + 1
        new_window.setWindowTitle(self.ui_messages.default_doc_name
                                  + str(self._new_count))
        new_window.show()

    def _handle_save(self):
        pass

    def get_file_extension_filters(self):
        return [self._formats[fmt].FILTER_STRING for fmt in self._formats]

    def get_format_by_filename(self, filename):
        extension = os.path.splitext(str(filename))[1]
        for fmt in self._formats:
            if extension.lower() in self._formats[fmt].FILE_EXTENSIONS:
                return self._formats[fmt]
        return self._formats[self.DEFAULT_FORMAT_MODULENAME] 

    def _handle_save_as(self):
        if not self.get_active_canvas():
            return
        filters = self.get_file_extension_filters()
        filter_string = ";;".join(filters)
        dflt = self._formats[self.DEFAULT_FORMAT_MODULENAME].FILTER_STRING
        path = QtGui.QFileDialog.getSaveFileName(self,
                                                 self.ui_messages.save_as,
                                                 filter = filter_string,
                                                 selectedFilter = dflt)
        if not path:
            return

        fmt = self.get_format_by_filename(path)
        fmt.save(path, self.get_active_canvas())

    def _handle_open(self):
        filters = self.get_file_extension_filters()
        all_extensions = []
        for fmt in self._formats:
            all_extensions += self._formats[fmt].FILE_EXTENSIONS
        all_extensions = ["*%s" % e for e in all_extensions]
        all_extensions = " ".join(all_extensions)
        filter_all = "%s (%s)" % (self.ui_messages.all_supported_types,
                                  all_extensions)
        filters.insert(0, filter_all)
        filter_string = ";;".join(filters)
        path_list = QtGui.QFileDialog.getOpenFileNames(self,
                                                  self.ui_messages.open_drwg,
                                                  filter = filter_string,
                                                  selectedFilter = filter_all)
        if not path_list:
            return
        for path in path_list:
            fmt = self.get_format_by_filename(path)
            document = drawing.Document()
            new_canvas = drawing.Canvas(self.get_tool(self.DEFAULT_TOOL_CLASSNAME),
                                        document)
            new_window = self.ui.mdiArea.addSubWindow(new_canvas)
            new_window.setWindowTitle(path)
            fmt.load(str(path), new_canvas)
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

        self.save_as = QtGui.QApplication.translate("UiMessages",
            "Save As",
            None,
            QtGui.QApplication.UnicodeUTF8)

        self.all_supported_types = QtGui.QApplication.translate("UiMessages",
            "All supported file types",
            None,
            QtGui.QApplication.UnicodeUTF8)

        self.open_drwg = QtGui.QApplication.translate("UiMessages",
            "Open Drawing",
            None,
            QtGui.QApplication.UnicodeUTF8)
