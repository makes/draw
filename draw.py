from PyQt4 import QtCore, QtGui
import os.path
import functools
import inspect
import pkgutil

from ui.draw_main_window import Ui_MainWindow
from preferences import PreferencesDialog

import drawing
import drawing.tools

import formats

class DrawMainWindow(QtGui.QMainWindow):
    DEFAULT_TOOL_CLASSNAME = "Pen"
    DEFAULT_FORMAT_MODULENAME = "svg"

    def __init__(self, lang):
        self.ui_messages = UiMessages()
        self.lang = lang
        self.new_count = 0
        self.current_tool = None

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
            if module.ENABLED:
                self._formats[modname] = module

        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create undo stuff
        self.undo = QtGui.QUndoGroup(self)
        self.update_undo_actions(self.ui.actionUndo, self.ui.actionRedo)

        # Add selector action info to each tool.
        # TODO tools should be fully dynamic to avoid this.
        #      for now it doesn't matter as there are only a few.
        self.get_tool("Pick").selector = self.ui.actionSelectPickTool
        self.get_tool("Pen").selector = self.ui.actionSelectPenTool
        self.get_tool("Rect").selector = \
            self.ui.actionSelectRectangleTool
        self.get_tool("Ellipse").selector = self.ui.actionSelectEllipseTool
        self.get_tool("Text").selector = self.ui.actionSelectTextTool

        # Create a mutually exclusive action group for drawing tools
        self.ui.tool_selectors = QtGui.QActionGroup(self)
        self.ui.tool_selectors.setExclusive(True)
        self.ui.tool_selectors.addAction(self.ui.actionSelectPickTool)
        self.ui.tool_selectors.addAction(self.ui.actionSelectPenTool)
        self.ui.tool_selectors.addAction(self.ui.actionSelectRectangleTool)
        self.ui.tool_selectors.addAction(self.ui.actionSelectEllipseTool)
        self.ui.tool_selectors.addAction(self.ui.actionSelectTextTool)

        self._connect_slots()
        self._init_interface()

    def _connect_slots(self):
        self.ui.actionNew.triggered.connect(self.new_drawing)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSaveAs.triggered.connect(self.save_as)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionClose.triggered.connect(self.close_active_subwindow)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionCascadeWindows.triggered.connect(
            self.ui.mdiArea.cascadeSubWindows)
        self.ui.actionTileWindows.triggered.connect(
            self.ui.mdiArea.tileSubWindows)
        self.ui.actionPreferences.triggered.connect(self.preferences)

        # TODO make tools load dynamically
        self.ui.actionSelectPickTool.triggered.connect(
            functools.partial(self.set_current_tool, self.get_tool("Pick")))
        self.ui.actionSelectPenTool.triggered.connect(
            functools.partial(self.set_current_tool, self.get_tool("Pen")))
        self.ui.actionSelectRectangleTool.triggered.connect(
            functools.partial(self.set_current_tool, self.get_tool("Rect")))
        self.ui.actionSelectEllipseTool.triggered.connect(
            functools.partial(self.set_current_tool, self.get_tool("Ellipse")))
        self.ui.actionSelectTextTool.triggered.connect(
            functools.partial(self.set_current_tool, self.get_tool("Text")))

        self.ui.mdiArea.subWindowActivated.connect(
                self.subwindow_focus_changed)

        self.ui.menuWindow.aboutToShow.connect(self.update_window_menu)

    def _init_interface(self):
        self.show()

    def update_file_actions(self, canvas):
        if not canvas:
            self.ui.actionSave.setEnabled(False)
            self.ui.actionSaveAs.setEnabled(False)
            self.ui.actionClose.setEnabled(False)
        elif canvas.is_clean():
            self.ui.actionSave.setEnabled(False)
        else:
            self.ui.actionSave.setEnabled(True)
            self.ui.actionSaveAs.setEnabled(True)

    def clean_changed(self, clean):
        self.update_file_actions(self.get_active_canvas())

    def new_subwindow(self, document = None):
        if not document:
            document = drawing.Document()
        new_canvas = drawing.Canvas(self.get_tool(self.DEFAULT_TOOL_CLASSNAME),
                                    document)
        self.undo.addStack(new_canvas.get_undo_stack())
        new_canvas.setSceneRect(0, 0, 10000, 10000)
        new_window = drawing.Window(self, self.ui.mdiArea, new_canvas)
        new_window.window_closed.connect(self.subwindow_closed)
        new_window.canvas.clean_changed.connect(self.clean_changed)
        self.ui.actionClose.setEnabled(True)
        self.ui.actionSaveAs.setEnabled(True)
        new_window.showMaximized()
        return new_window

    def close_active_subwindow(self):
        window = self.get_active_subwindow()
        if not window:
            return False
        window.close()

    def subwindow_closed(self, window):
        self.ui.mdiArea.removeSubWindow(window)
        self.undo.removeStack(window.canvas.get_undo_stack())

    def closeEvent(self, event):
        confirmed = True
        for window in self.get_subwindows():
            self.set_active_subwindow(window)
            confirmed = window.close()
            if not confirmed:
                event.ignore()
                return
        event.accept()

    def preferences(self):
        dialog = PreferencesDialog(self,
                                   self.lang.languages,
                                   self.lang.get_current_language_index())
        if dialog.exec_():
            self.lang.select(dialog.get_language())

    def new_drawing(self):
        new_window = self.new_subwindow()
        self.new_count = self.new_count + 1
        new_window.setWindowTitle(self.ui_messages.default_doc_name
                                  + str(self.new_count))
        new_window.show()

    def save(self):
        canvas = self.get_active_canvas()
        if not canvas:
            return False
        if not canvas.filename:
            return self.save_as()
        else:
            self.deactivate_current_tool()
            fmt = self.get_format_by_filename(canvas.filename)
            fmt.save(canvas.filename, canvas)
            canvas.set_clean()
            return True

    def get_file_extension_filters(self, operation):
        filters = []
        for fmt in self._formats:
            if operation in self._formats[fmt].__dict__:
                filters.append(self._formats[fmt].FILTER_STRING)
        return filters

    def get_format_by_filename(self, filename):
        extension = os.path.splitext(str(filename))[1]
        for fmt in self._formats:
            if extension.lower() in self._formats[fmt].FILE_EXTENSIONS:
                return self._formats[fmt]
        return self._formats[self.DEFAULT_FORMAT_MODULENAME] 

    def save_as(self):
        canvas = self.get_active_canvas()
        if not canvas:
            return False
        self.deactivate_current_tool()
        filters = self.get_file_extension_filters('save')
        filter_string = ";;".join(filters)
        dflt = self._formats[self.DEFAULT_FORMAT_MODULENAME].FILTER_STRING
        path = QtGui.QFileDialog.getSaveFileName(self,
                                                 self.ui_messages.save_as,
                                                 filter = filter_string,
                                                 selectedFilter = dflt)
        if not path:
            return False

        fmt = self.get_format_by_filename(path)
        fmt.save(path, self.get_active_canvas())
        self.get_active_subwindow().filename = path
        canvas.set_clean()
        return True

    def open(self):
        filters = self.get_file_extension_filters('load')
        all_extensions = []
        for fmt in self._formats:
            if 'load' in self._formats[fmt].__dict__:
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
            new_window = self.new_subwindow(document)
            new_window.filename = path
            fmt.load(str(path), new_window.get_canvas())
            new_window.show()

    def exit(self):
        self.close()

    def get_tool(self, name):
        if name in self._tools:
            return self._tools[name]
        else:
            return None

    def clear_tool_selection(self):
        self.reset_current_tool()
        for action in self.ui.tool_selectors.actions():
            action.setChecked(False)
        self.ui.toolOptionsDock.setWidget(None)
        self.current_tool = None

    def update_tool_buttons(self, tool):
        """ Make sure the correct tool button shows as pressed """
        for action in self.ui.tool_selectors.actions():
            if tool.selector is action:
                action.setChecked(True)
                return

    def reset_current_tool(self):
        if self.current_tool:
            self.current_tool.reset()

    def deactivate_current_tool(self):
        if self.current_tool:
            self.current_tool.deactivate()

    def set_current_tool(self, tool):
        canvas = self.get_active_canvas()
        self.reset_current_tool()
        if not canvas:
            self.ui.toolOptionsDock.setWidget(None)
            self.ui.statusbar.clearMessage()
            self.ui.statusbar.showMessage(self.ui_messages.tool_unavailable,
                                          8000)
            self.clear_tool_selection()
            return
        if self.current_tool is not tool:
            self.ui.toolOptionsDock.setWidget(None)
            self.ui.statusbar.clearMessage()
            self.ui.statusbar.showMessage(self.ui_messages.selected_tool + ": "
                                          + tool.get_name(), 3000)
            self.update_tool_buttons(tool)
            self.ui.toolOptionsDock.setWidget(tool.options_widget)
        self.current_tool = canvas.set_current_tool(tool)

    def get_active_canvas(self):
        window = self.get_active_subwindow()
        if not window:
            return None
        return window.widget()

    def get_active_subwindow(self):
        return self.ui.mdiArea.activeSubWindow()

    def set_active_subwindow(self, window):
        self.ui.mdiArea.setActiveSubWindow(window)

    def get_subwindows(self):
        return self.ui.mdiArea.subWindowList()

    def update_window_menu(self):
        self.ui.menuWindow.clear()
        windows = self.get_subwindows()

        self.ui.menuWindow.addAction(self.ui.actionCascadeWindows)
        self.ui.menuWindow.addAction(self.ui.actionTileWindows)
        if len(windows) > 0:
            self.ui.menuWindow.addSeparator()

        if len(windows) <= 1:
            self.ui.actionCascadeWindows.setEnabled(False)
            self.ui.actionTileWindows.setEnabled(False)
        else:
            self.ui.actionCascadeWindows.setEnabled(True)
            self.ui.actionTileWindows.setEnabled(True)

        for window in windows:
            action = self.ui.menuWindow.addAction(window.windowTitle())
            action.setCheckable(True)
            action.setChecked(window == self.get_active_subwindow())
            action.triggered.connect(
                functools.partial(self.set_active_subwindow, window))

    def subwindow_focus_changed(self):
        canvas = self.get_active_canvas()
        self.update_file_actions(canvas)
        if not canvas:
            self.clear_tool_selection()
            self.undo.setActiveStack(None)
            return
        self.set_current_tool(canvas.tool)
        self.current_tool = canvas.tool
        self.undo.setActiveStack(canvas.get_undo_stack())

    def update_undo_actions(self, old_undo, old_redo):
        """ A workaround for translation bug QTBUG-7324 """
        # Grab icon, tooltip, etc. from data created in Qt Designer
        undo_action = self.undo.createUndoAction(self,
                                                 old_undo.text())
        undo_action.setIcon(old_undo.icon())
        undo_action.setToolTip(old_undo.toolTip())
        undo_action.setShortcut(old_undo.shortcut())
        undo_action.setObjectName(old_undo.objectName())
        redo_action = self.undo.createRedoAction(self,
                                                 old_redo.text())
        redo_action.setIcon(old_redo.icon())
        redo_action.setToolTip(old_redo.toolTip())
        redo_action.setShortcut(old_redo.shortcut())
        redo_action.setObjectName(old_redo.objectName())

        # Replace original actions with the newly created ones
        self.ui.actionUndo = undo_action
        self.ui.actionRedo = redo_action
        self.ui.menuEdit.insertAction(old_undo, self.ui.actionUndo)
        self.ui.menuEdit.removeAction(old_undo)
        self.ui.menuEdit.insertAction(old_redo, self.ui.actionRedo)
        self.ui.menuEdit.removeAction(old_redo)
        self.ui.mainToolBar.insertAction(old_undo, self.ui.actionUndo)
        self.ui.mainToolBar.removeAction(old_undo)
        self.ui.mainToolBar.insertAction(old_redo, self.ui.actionRedo)
        self.ui.mainToolBar.removeAction(old_redo)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.ui.retranslateUi(self)
            self.ui_messages.translate_messages()
            self.update_undo_actions(self.ui.actionUndo, self.ui.actionRedo)

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

