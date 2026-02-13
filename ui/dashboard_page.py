from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
)


class DashboardPage(QWidget):
    open_youtube = Signal()

    def __init__(self):
        super().__init__()

        self._cards = []  # keep references if you want hover effects later
        self.init_ui()

    # --- same shadow + card system as your YouTubeDownloaderPage ---
    def apply_shadow(self, widget, blur=30, x=0, y=10, opacity=120):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(x, y)
        shadow.setColor(QColor(0, 0, 0, opacity))
        widget.setGraphicsEffect(shadow)

    def card(self, layout=None):
        frame = QFrame()
        frame.setObjectName("Card")
        if layout is not None:
            frame.setLayout(layout)
        self.apply_shadow(frame, blur=35, x=0, y=12)
        return frame

    def init_ui(self):
        # Root matches your YouTube page root layout
        root = QHBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(16)

        # ===== Sidebar (same style & spacing as YouTube page) =====
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(12)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)

        brand = QLabel("Personal Use Only")
        brand.setObjectName("Brand")
        brand.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        tagline = QLabel("Tools for everyday media tasks")
        tagline.setObjectName("Tagline")

        # Minimal nav (you can add more later)
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

        help_box = QLabel("Tip: Click a tool to open it.\nMore tools coming soon ✨")
        help_box.setObjectName("HelpBox")
        sidebar_layout.addWidget(help_box)

        sidebar = self.card(sidebar_layout)
        sidebar.setFixedWidth(260)

        # ===== Main Area =====
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Hero card (exact same structure as YouTube page)
        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(6)
        hero_layout.setContentsMargins(22, 18, 22, 18)

        hero_title = QLabel("Homies Media Tools")
        hero_title.setObjectName("HeroTitle")

        hero_sub = QLabel("A minimal toolbox for video, audio, images and docs.")
        hero_sub.setObjectName("HeroSub")

        hero_layout.addWidget(hero_title)
        hero_layout.addWidget(hero_sub)

        hero = self.card(hero_layout)

        # Tools row (minimal & sleek: 2 large cards)
        tools_row = QHBoxLayout()
        tools_row.setSpacing(18)
        tools_row.setContentsMargins(18, 18, 18, 18)

        yt_card = self.tool_card(
            title="🎥  YouTube Downloader",
            desc="Download video/audio + thumbnail using yt-dlp.",
            primary_label="Open",
            primary_cb=self.open_youtube.emit,
        )

        coming_card = self.tool_card(
            title="🖼  Image Tools",
            desc="Compress, convert, resize (coming soon).",
            primary_label="Coming soon",
            primary_cb=None,
            disabled=True,
        )

        tools_row.addWidget(yt_card, 1)
        tools_row.addWidget(coming_card, 1)

        tools_card = self.card(tools_row)

        # Status-like footer card (optional but matches your vibe)
        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(8)
        footer_layout.setContentsMargins(18, 16, 18, 16)

        footer = QLabel("Choose a tool from the cards above or the sidebar.")
        footer.setObjectName("Status")

        footer_layout.addWidget(footer)
        footer_card = self.card(footer_layout)

        main_layout.addWidget(hero)
        main_layout.addWidget(tools_card)
        main_layout.addStretch(1)
        main_layout.addWidget(footer_card)

        main = QFrame()
        main.setLayout(main_layout)
        main.setObjectName("MainWrap")

        root.addWidget(sidebar)
        root.addWidget(main, 1)

        # Sidebar interactions
        btn_youtube.clicked.connect(self.open_youtube.emit)

    def tool_card(self, title: str, desc: str, primary_label: str, primary_cb, disabled: bool = False):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(18, 18, 18, 18)

        title_label = QLabel(title)
        title_label.setObjectName("VideoTitle")
        title_label.setWordWrap(True)

        desc_label = QLabel(desc)
        desc_label.setObjectName("Hint")
        desc_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch(1)

        btn = QPushButton(primary_label)
        btn.setObjectName("PrimaryBtn")
        if disabled:
            btn.setEnabled(False)
        elif primary_cb:
            btn.clicked.connect(primary_cb)

        layout.addWidget(btn)

        frame = self.card(layout)
        self._cards.append(frame)
        return frame
