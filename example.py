from PySide6 import QtCore, QtWidgets, QtGui
from Glassmorphism import *

def coloredIcon(color: QtGui.QColor, icon_path: str, size: QtCore.QSize, scale: int = 2):
    icon = QtGui.QPixmap(size.width() * scale, size.height() * scale)
    pixmap_icon = QtGui.QPixmap(icon_path)

    icon.fill(color)
    painter = QtGui.QPainter(icon)
    painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
    painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_DestinationIn)
    painter.drawPixmap(0, 0, size.width() * scale, size.height() * scale, pixmap_icon)
    painter.end()

    return icon

class Icons_with_BackDrop(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        ml = QtWidgets.QHBoxLayout()
        ml.setContentsMargins(100, 200, 100, 100)
        ml.setSpacing(10)

        self.bg_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("resources/bg.jpeg")
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents( True )
        self.bg_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored)
        self.setLayout(ml)

        grad = QtGui.QLinearGradient(0, 0, 1, 1)
        grad.setCoordinateMode(QtGui.QLinearGradient.CoordinateMode.ObjectMode)
        grad.setStops([(0, QtGui.QColor(255, 255, 255, 255)), (0.35, QtGui.QColor(255, 255, 255, 125)), (0.65, QtGui.QColor(255, 255, 255, 125)), (1, QtGui.QColor(255, 255, 255, 255))])

        backgrounds=[{"background-color": grad, "border": QtGui.QColor("#FFFFFF"),"border-width": 2, "opacity": .4}]

        icons = ["resources/icons/chat.svg", "resources/icons/images.svg", "resources/icons/music.svg", "resources/icons/phone.svg", "resources/icons/wifi.svg"]
        for icon in icons:
            size = QtCore.QSize(50, 50)
            btn = QtWidgets.QPushButton()
            btn.setIcon(coloredIcon(QtGui.QColor(254, 1, 154), icon, size))
            btn.setIconSize(size)
            btn.setStyleSheet("border:none; padding: 20px;")
            ml.addWidget(btn)
            bdw = BackDropWrapper(btn, 10, 20, backgrounds)
            bdw.enable_shine_animation(angle=135, color=QtGui.QColor(255, 255, 255, 90))
            bdw.enable_move_animation(offset=(0, -30))
            ml.addWidget(bdw)

        self.show()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.bg_label.setFixedSize(event.size())

app = QtWidgets.QApplication([])
app.setStyle("Fusion")
w = Icons_with_BackDrop()
app.exec()
