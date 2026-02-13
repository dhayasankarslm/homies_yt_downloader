from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from ui.youtube_page import YouTubeDownloaderPage
from ui.dashboard_page import DashboardPage


class MediaApp(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("Homies Media Tools")
    self.setMinimumSize(1200, 750)

    self.pages = QStackedWidget()

    self.dashboard = DashboardPage()
    self.youtube_page = YouTubeDownloaderPage()

    self.pages.addWidget(self.dashboard)
    self.pages.addWidget(self.youtube_page)

    layout = QVBoxLayout(self)
    layout.addWidget(self.pages)

    self.dashboard.open_youtube.connect(
      lambda: self.pages.setCurrentIndex(1)
    )
