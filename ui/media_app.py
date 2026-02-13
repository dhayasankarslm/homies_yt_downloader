from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QPushButton
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from ui.styles import get_stylesheet
from ui.dashboard_page import DashboardPage
from ui.youtube_page import YouTubeDownloaderPage
from ui.ui_helpers import create_card


class MediaApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Homies Media Tools")
        self.setMinimumSize(1200, 750)

        font = QFont("Segoe UI")
        font.setPointSize(10)
        self.setFont(font)
        self.setStyleSheet(get_stylesheet())

        root = QHBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(16)

        # ===== SIDEBAR =====
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(12)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)

        brand = QLabel("Personal Use Only")
        brand.setObjectName("Brand")

        tagline = QLabel("Media Toolkit")
        tagline.setObjectName("Tagline")

        self.btn_home = QPushButton("🏠  Home")
        self.btn_home.setObjectName("SideBtn")

        self.btn_youtube = QPushButton("🎥  YouTube")
        self.btn_youtube.setObjectName("SideBtn")

        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(tagline)
        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(self.btn_home)
        sidebar_layout.addWidget(self.btn_youtube)
        sidebar_layout.addStretch(1)

        help_box = QLabel("Select a tool from the sidebar.")
        help_box.setObjectName("HelpBox")
        sidebar_layout.addWidget(help_box)

        sidebar = create_card(sidebar_layout)
        sidebar.setFixedWidth(260)

        # ===== PAGES =====
        self.pages = QStackedWidget()

        self.dashboard = DashboardPage()
        self.youtube = YouTubeDownloaderPage()

        self.pages.addWidget(self.dashboard)  # index 0
        self.pages.addWidget(self.youtube)    # index 1

        root.addWidget(sidebar)
        root.addWidget(self.pages, 1)

        # ===== NAVIGATION =====
        self.btn_home.clicked.connect(lambda: self.switch_page(0))
        self.btn_youtube.clicked.connect(lambda: self.switch_page(1))

        self.switch_page(0)

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)

        self.btn_home.setProperty("active", index == 0)
        self.btn_youtube.setProperty("active", index == 1)

        self.btn_home.style().unpolish(self.btn_home)
        self.btn_home.style().polish(self.btn_home)

        self.btn_youtube.style().unpolish(self.btn_youtube)
        self.btn_youtube.style().polish(self.btn_youtube)
