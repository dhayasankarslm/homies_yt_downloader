from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout,
    QGridLayout, QFrame, QPushButton
)
from PySide6.QtGui import QFont


class DashboardPage(QWidget):

    open_youtube = Signal()

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(60, 40, 60, 40)
        root.setSpacing(30)

        # ===== HERO SECTION =====
        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(6)

        title = QLabel("Homies Media Tools")
        title.setObjectName("HeroTitle")

        subtitle = QLabel("Your personal offline toolkit")
        subtitle.setObjectName("HeroSub")

        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)

        hero = QFrame()
        hero.setLayout(hero_layout)
        hero.setObjectName("Card")

        root.addWidget(hero)

        # ===== TOOL GRID =====
        grid = QGridLayout()
        grid.setSpacing(24)

        yt_card = self.create_tool_card(
            "🎥 YouTube Downloader",
            "Download videos and audio",
            self.open_youtube.emit
        )

        grid.addWidget(yt_card, 0, 0)

        # Future tools (placeholder)
        img_card = self.create_tool_card(
            "🖼 Image Tools",
            "Coming soon",
            None
        )

        grid.addWidget(img_card, 0, 1)

        grid_wrap = QFrame()
        grid_wrap.setLayout(grid)

        root.addWidget(grid_wrap)
        root.addStretch(1)

    def create_tool_card(self, title, desc, callback):
        frame = QFrame()
        frame.setObjectName("Card")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size:18px; font-weight:800;")

        desc_label = QLabel(desc)
        desc_label.setStyleSheet("font-size:12px; color: rgba(226,232,240,0.7);")

        btn = QPushButton("Open")
        btn.setObjectName("PrimaryBtn")

        if callback:
            btn.clicked.connect(callback)
        else:
            btn.setEnabled(False)

        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch(1)
        layout.addWidget(btn)

        return frame
