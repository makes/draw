call pyuic4 -o ui\draw_main_window.py ui\draw_main_window.ui
call pyrcc4 -o ui\images_rc.py ui\images.qrc
pylupdate4 translate.pro
lrelease translate.pro

