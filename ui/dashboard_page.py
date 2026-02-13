from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout

class DashboardPage(QWidget):

    open_youtube = Signal()   # ✅ class-level signal

    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)

        yt_btn = QPushButton("🎥 YouTube Downloader")

        yt_btn.clicked.connect(self.open_youtube)  # ✅ correct

        layout.addWidget(yt_btn, 0, 0)
