from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from utils.helpers import resource_path


class SplashScreen(QWidget):
  finished = Signal()

  def __init__(self):
    super().__init__()
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
    self.setAttribute(Qt.WA_TranslucentBackground)

    layout = QVBoxLayout(self)
    layout.setContentsMargins(0, 0, 0, 0)

    self.label = QLabel()
    pixmap = QPixmap(resource_path("splash.png"))
    self.label.setPixmap(pixmap)
    self.label.setAlignment(Qt.AlignCenter)

    layout.addWidget(self.label)

    self.setWindowOpacity(0.0)

  def start_animation(self):
    self.show()
    self.anim = QPropertyAnimation(self, b"windowOpacity")
    self.anim.setDuration(800)
    self.anim.setStartValue(0.0)
    self.anim.setEndValue(1.0)
    self.anim.setEasingCurve(QEasingCurve.OutCubic)
    self.anim.finished.connect(self.wait_and_fade_out)
    self.anim.start()

  def wait_and_fade_out(self):
    QTimer.singleShot(1500, self.fade_out)

  def fade_out(self):
    self.anim = QPropertyAnimation(self, b"windowOpacity")
    self.anim.setDuration(800)
    self.anim.setStartValue(1.0)
    self.anim.setEndValue(0.0)
    self.anim.setEasingCurve(QEasingCurve.InCubic)
    self.anim.finished.connect(self.close)
    self.anim.finished.connect(self.finished.emit)
    self.anim.start()
