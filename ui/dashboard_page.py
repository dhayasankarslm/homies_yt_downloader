from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
  QWidget, QLabel, QPushButton,
  QVBoxLayout, QHBoxLayout
)

from ui.ui_helpers import create_card


class DashboardPage(QWidget):
  open_youtube = Signal()

  def __init__(self):
    super().__init__()
    self.init_ui()

  def init_ui(self):
    root = QHBoxLayout(self)
    root.setContentsMargins(18, 18, 18, 18)
    root.setSpacing(16)


    sidebar_layout = QVBoxLayout()
    sidebar_layout.setSpacing(12)
    sidebar_layout.setContentsMargins(16, 16, 16, 16)

    brand = QLabel("Personal Use Only")
    brand.setObjectName("Brand")

    tagline = QLabel("Tools for everyday media tasks")
    tagline.setObjectName("Tagline")

    btn_home = QPushButton("🏠  Home")
    btn_home.setObjectName("SideBtn")
    btn_home.setProperty("active", True)

    btn_youtube = QPushButton("🎥  YouTube")
    btn_youtube.setObjectName("SideBtn")

    sidebar_layout.addWidget(brand)
    sidebar_layout.addWidget(tagline)
    sidebar_layout.addSpacing(10)
    sidebar_layout.addWidget(btn_home)
    sidebar_layout.addWidget(btn_youtube)
    sidebar_layout.addStretch(1)

    help_box = QLabel("Tip: Click a tool to open it.")
    help_box.setObjectName("HelpBox")
    sidebar_layout.addWidget(help_box)

    sidebar = create_card(sidebar_layout)
    sidebar.setFixedWidth(260)


    main_layout = QVBoxLayout()
    main_layout.setSpacing(16)
    main_layout.setContentsMargins(0, 0, 0, 0)

    hero_layout = QVBoxLayout()
    hero_layout.setSpacing(6)
    hero_layout.setContentsMargins(22, 18, 22, 18)

    hero_title = QLabel("Homies Media Tools")
    hero_title.setObjectName("HeroTitle")

    hero_sub = QLabel("A minimal toolbox for video, audio and more.")
    hero_sub.setObjectName("HeroSub")

    hero_layout.addWidget(hero_title)
    hero_layout.addWidget(hero_sub)

    hero = create_card(hero_layout)

    tools_layout = QHBoxLayout()
    tools_layout.setSpacing(18)
    tools_layout.setContentsMargins(18, 18, 18, 18)

    yt_card = self.build_tool_card(
      "🎥  YouTube Downloader",
      "Download video/audio + thumbnails",
      self.open_youtube.emit
    )

    tools_layout.addWidget(yt_card)

    tools_card = create_card(tools_layout)

    main_layout.addWidget(hero)
    main_layout.addWidget(tools_card)
    main_layout.addStretch(1)

    root.addWidget(sidebar)
    root.addLayout(main_layout, 1)

    btn_youtube.clicked.connect(self.open_youtube.emit)

  def build_tool_card(self, title, desc, callback):
    layout = QVBoxLayout()
    layout.setSpacing(10)
    layout.setContentsMargins(18, 18, 18, 18)

    title_label = QLabel(title)
    title_label.setObjectName("VideoTitle")

    desc_label = QLabel(desc)
    desc_label.setObjectName("Hint")

    btn = QPushButton("Open")
    btn.setObjectName("PrimaryBtn")
    btn.clicked.connect(callback)

    layout.addWidget(title_label)
    layout.addWidget(desc_label)
    layout.addStretch(1)
    layout.addWidget(btn)

    return create_card(layout)
