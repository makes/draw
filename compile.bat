call pyuic4 -o ui\draw_main_window.py ui\draw_main_window.ui
call pyuic4 -o ui\tool_options_pen.py ui\tool_options_pen.ui
call pyuic4 -o ui\tool_options_rect.py ui\tool_options_rect.ui
call pyuic4 -o ui\tool_options_ellipse.py ui\tool_options_ellipse.ui
call pyrcc4 -o ui\images_rc.py ui\images.qrc
type NUL > ui\__init__.py
pylupdate4 translate.pro
lrelease translate.pro

