from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer, Signal
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QProgressBar

from utils.helpers import resource_path


class SplashScreen(QWidget):
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.label = QLabel()
        pixmap = QPixmap(resource_path("splash.png"))
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setFixedHeight(25)
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        with open("ui/splash_style.qss", "r") as f:
          self.progress.setStyleSheet(f.read())

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        self.setWindowOpacity(0.0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def center_on_screen(self):
      screen = QGuiApplication.primaryScreen()
      screen_geometry = screen.availableGeometry()

      splash_geometry = self.frameGeometry()
      splash_geometry.moveCenter(screen_geometry.center())

      self.move(splash_geometry.topLeft())

    def start_animation(self):
        self.adjustSize()
        self.center_on_screen()
        self.show()

        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(800)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.finished.connect(self.start_loading)
        self.anim.start()

    def start_loading(self):
        self.timer.start(20)

    def update_progress(self):
        value = self.progress.value() + 1
        self.progress.setValue(value)

        if value >= 100:
            self.timer.stop()
            QTimer.singleShot(300, self.fade_out)

    def fade_out(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(800)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.finished.connect(self.close)
        self.anim.finished.connect(self.finished.emit)
        self.anim.start()
