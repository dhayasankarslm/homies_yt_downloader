from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from ui.ui_helpers import create_card


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        # ===== HERO =====
        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(6)
        hero_layout.setContentsMargins(22, 18, 22, 18)

        hero_title = QLabel("Homies Media Tools")
        hero_title.setObjectName("HeroTitle")

        hero_sub = QLabel("A minimal offline toolkit.")
        hero_sub.setObjectName("HeroSub")

        hero_layout.addWidget(hero_title)
        hero_layout.addWidget(hero_sub)

        hero = create_card(hero_layout)

        # ===== FEATURE CARD =====
        feature_row = QHBoxLayout()
        feature_row.setSpacing(18)
        feature_row.setContentsMargins(18, 18, 18, 18)

        yt_layout = QVBoxLayout()
        yt_layout.setSpacing(10)
        yt_layout.setContentsMargins(18, 18, 18, 18)

        yt_title = QLabel("🎥  YouTube Downloader")
        yt_title.setObjectName("VideoTitle")

        yt_desc = QLabel("Download videos, audio and thumbnails.")
        yt_desc.setObjectName("Hint")

        yt_layout.addWidget(yt_title)
        yt_layout.addWidget(yt_desc)
        yt_layout.addStretch(1)

        yt_card = create_card(yt_layout)

        feature_row.addWidget(yt_card)

        feature_card = create_card(feature_row)

        root.addWidget(hero)
        root.addWidget(feature_card)
        root.addStretch(1)
