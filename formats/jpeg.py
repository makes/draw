from PyQt4 import QtCore, QtGui

ENABLED = True
FILE_EXTENSIONS = ['.jpg', '.jpeg']
FILTER_STRING = "JPEG (*.jpg *.jpeg)"

def save(filename, canvas):
    bounds = canvas.document.itemsBoundingRect()
    view = QtGui.QGraphicsView()
    view.setScene(canvas.document)
    view.fitInView(bounds, QtCore.Qt.KeepAspectRatio)
    image = QtGui.QImage(bounds.width(),
                         bounds.height(),
                         QtGui.QImage.Format_ARGB32_Premultiplied)
    image.fill(QtCore.Qt.white)
    painter = QtGui.QPainter(image)
    painter.setRenderHints(QtGui.QPainter.Antialiasing |
                           QtGui.QPainter.SmoothPixmapTransform)
    view.render(painter)
    painter.end()
    image.save(filename, "JPG", 100)

