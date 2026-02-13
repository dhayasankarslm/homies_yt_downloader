from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QApplication

from ui.dashboard_page import DashboardPage
from ui.styles import get_stylesheet
from ui.youtube_page import YouTubeDownloaderPage


class MediaApp(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("Homies Media Tools")
    self.setMinimumSize(1100, 700)

    font = QFont("Segoe UI")
    font.setPointSize(10)
    QApplication.instance().setFont(font)
    self.setStyleSheet(get_stylesheet())

    self.pages = QStackedWidget()

    self.dashboard = DashboardPage()
    self.youtube = YouTubeDownloaderPage()

    self.pages.addWidget(self.dashboard)  # index 0
    self.pages.addWidget(self.youtube)  # index 1

    self.dashboard.open_youtube.connect(
      lambda: self.pages.setCurrentIndex(1)
    )

    self.youtube.go_home.connect(
      lambda: self.pages.setCurrentIndex(0)
    )

    layout = QVBoxLayout(self)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.pages)
