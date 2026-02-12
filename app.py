import sys
from io import BytesIO
import os

import requests
from PIL import Image
from yt_dlp import YoutubeDL

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QComboBox, QFileDialog, QFrame,
    QStackedWidget, QProgressBar, QGraphicsDropShadowEffect, QSizePolicy, QSplashScreen
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QPixmap, QFont, QIcon


def resource_path(relative_path: str):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class DownloadThread(QThread):
    progress_text = pyqtSignal(str)
    progress_value = pyqtSignal(int)
    finished_signal = pyqtSignal(str)

    def __init__(self, url, ydl_opts):
        super().__init__()
        self.url = url
        self.ydl_opts = ydl_opts
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        def progress_hook(d):
            if self._cancel:
                raise Exception("Download cancelled")

            if d.get("status") == "downloading":
                downloaded = d.get("downloaded_bytes", 0)
                total = d.get("total_bytes") or d.get("total_bytes_estimate")

                if total:
                    percent = int((downloaded / total) * 100)
                    speed = d.get("speed")
                    eta = d.get("eta")

                    speed_txt = ""
                    if speed:
                        speed_txt = f" • {speed/1024/1024:.2f} MB/s"
                    eta_txt = ""
                    if eta:
                        eta_txt = f" • ETA {eta}s"

                    self.progress_value.emit(percent)
                    self.progress_text.emit(f"Downloading… {percent}%{speed_txt}{eta_txt}")

        self.ydl_opts["progress_hooks"] = [progress_hook]

        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([self.url])

            if not self._cancel:
                self.finished_signal.emit("Download complete ✅")

        except Exception as e:
            if self._cancel:
                self.finished_signal.emit("Download cancelled ❌")
            else:
                self.finished_signal.emit(f"Error: {e}")

    
class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HOMIES YOUTUBE Downloader")
        self.setMinimumSize(1100, 700)

        self.setWindowIcon(QIcon(resource_path("homies_yt_downloader_icon.ico")))


        self.current_url = None
        self.thumbnail_url = None
        self.video_formats = {}
        self.audio_formats = {}
        self.thread = None

        self._fade_anim = None

        self.init_ui()
        self.apply_style()



    def apply_shadow(self, widget, blur=30, x=0, y=10, opacity=120):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(x, y)
        shadow.setColor(Qt.black)
        widget.setGraphicsEffect(shadow)
        widget.graphicsEffect().setEnabled(True)

    def card(self, layout=None):
        frame = QFrame()
        frame.setObjectName("Card")
        if layout is not None:
            frame.setLayout(layout)
        self.apply_shadow(frame, blur=35, x=0, y=12)
        return frame

    def fade_in_widget(self, widget):
        if not widget:
            return
        w = widget
        start = w.geometry()
        end = w.geometry().adjusted(0, -6, 0, -6)
        anim = QPropertyAnimation(w, b"geometry")
        anim.setDuration(220)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.start()
        self._fade_anim = anim  

    def init_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(16)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(12)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)

        brand = QLabel("Personal Use Only")
        brand.setObjectName("Brand")
        brand.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        tagline = QLabel("Piracy is wrong")
        tagline.setObjectName("Tagline")

        self.btn_video_mode = QPushButton("🎥  Video")
        self.btn_audio_mode = QPushButton("🎧  Audio")
        self.btn_video_mode.setObjectName("SideBtn")
        self.btn_audio_mode.setObjectName("SideBtn")

        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(tagline)
        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(self.btn_video_mode)
        sidebar_layout.addWidget(self.btn_audio_mode)
        sidebar_layout.addStretch(1)

        help_box = QLabel("Tip: Paste a YouTube link\nand press Fetch.")
        help_box.setObjectName("HelpBox")
        sidebar_layout.addWidget(help_box)

        sidebar = self.card(sidebar_layout)
        sidebar.setFixedWidth(260)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(0, 0, 0, 0)

        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(6)
        hero_layout.setContentsMargins(22, 18, 22, 18)

        hero_title = QLabel("Homies YouTube Downloader")
        hero_title.setObjectName("HeroTitle")

        hero_sub = QLabel("Download any youtube videos and audios;)")
        hero_sub.setObjectName("HeroSub")

        hero_layout.addWidget(hero_title)
        hero_layout.addWidget(hero_sub)
        hero = self.card(hero_layout)

        url_layout = QHBoxLayout()
        url_layout.setSpacing(12)
        url_layout.setContentsMargins(18, 16, 18, 16)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube link here…")

        self.fetch_btn = QPushButton("⚡ Fetch")
        self.clear_btn = QPushButton("🧹 Clear")
        self.cancel_btn = QPushButton("🛑 Cancel")

        self.fetch_btn.setObjectName("PrimaryBtn")
        self.clear_btn.setObjectName("GhostBtn")
        self.cancel_btn.setObjectName("GhostBtn")

        url_layout.addWidget(self.url_input, 1)
        url_layout.addWidget(self.fetch_btn)
        url_layout.addWidget(self.clear_btn)
        url_layout.addWidget(self.cancel_btn)
        url_card = self.card(url_layout)

        media_layout = QHBoxLayout()
        media_layout.setSpacing(18)
        media_layout.setContentsMargins(18, 18, 18, 18)

        thumb_wrap = QFrame()
        thumb_wrap.setObjectName("ThumbWrap")
        thumb_wrap.setFixedSize(420, 236)
        self.apply_shadow(thumb_wrap, blur=40, x=0, y=12)

        thumb_inner = QVBoxLayout(thumb_wrap)
        thumb_inner.setContentsMargins(10, 10, 10, 10)

        self.thumbnail_label = QLabel("Thumbnail preview")
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setObjectName("ThumbLabel")
        self.thumbnail_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        thumb_inner.addWidget(self.thumbnail_label)

        info_right = QVBoxLayout()
        info_right.setSpacing(10)

        self.title_label = QLabel("Paste a link and Fetch ✨")
        self.title_label.setObjectName("VideoTitle")
        self.title_label.setWordWrap(True)

        self.thumbnail_btn = QPushButton("🖼  Download Thumbnail")
        self.thumbnail_btn.setObjectName("PrimaryBtn")
        self.thumbnail_btn.hide()

        info_right.addWidget(self.title_label)
        info_right.addWidget(self.thumbnail_btn)
        info_right.addStretch(1)

        media_layout.addWidget(thumb_wrap, 0)
        media_layout.addLayout(info_right, 1)

        media_card = self.card(media_layout)

        self.pages = QStackedWidget()
        self.pages.setObjectName("Pages")

        self.video_page = self.build_video_page()
        self.audio_page = self.build_audio_page()

        self.pages.addWidget(self.video_page)
        self.pages.addWidget(self.audio_page)

        status_layout = QVBoxLayout()
        status_layout.setSpacing(10)
        status_layout.setContentsMargins(18, 16, 18, 16)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setObjectName("Progress")

        self.status_label = QLabel("Ready.")
        self.status_label.setObjectName("Status")

        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(self.status_label)
        status_card = self.card(status_layout)

        main_layout.addWidget(hero)
        main_layout.addWidget(url_card)
        main_layout.addWidget(media_card)
        main_layout.addWidget(self.pages, 1)
        main_layout.addWidget(status_card)

        main = QFrame()
        main.setLayout(main_layout)
        main.setObjectName("MainWrap")

        root.addWidget(sidebar)
        root.addWidget(main, 1)

        self.fetch_btn.clicked.connect(self.fetch_video)
        self.clear_btn.clicked.connect(self.clear_all)
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.thumbnail_btn.clicked.connect(self.download_thumbnail)

        self.btn_video_mode.clicked.connect(lambda: self.switch_page(0))
        self.btn_audio_mode.clicked.connect(lambda: self.switch_page(1))

    def build_video_page(self):
        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        row = QHBoxLayout()
        row.setSpacing(12)
        row.setContentsMargins(18, 18, 18, 18)

        self.video_format_combo = QComboBox()
        self.video_format_combo.addItems(["mp4", "webm"])

        self.resolution_combo = QComboBox()
        self.resolution_combo.setPlaceholderText("Resolution")

        self.video_download_btn = QPushButton("⬇️  Download Video")
        self.video_download_btn.setObjectName("PrimaryBtn")

        row.addWidget(self.video_format_combo, 1)
        row.addWidget(self.resolution_combo, 2)
        row.addWidget(self.video_download_btn, 1)

        card = self.card(row)

        hint = QLabel("Video mode: Choose container + resolution. Downloads best audio and merges automatically.")
        hint.setObjectName("Hint")

        layout.addWidget(card)
        layout.addWidget(hint)
        layout.addStretch(1)

        page = QFrame()
        page.setLayout(layout)

        self.video_format_combo.currentTextChanged.connect(self.update_video_resolutions)
        self.video_download_btn.clicked.connect(self.download_video)

        return page

    def build_audio_page(self):
        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        row = QHBoxLayout()
        row.setSpacing(12)
        row.setContentsMargins(18, 18, 18, 18)

        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(["mp3", "m4a", "webm"])

        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["best", "320k", "192k", "128k"])

        self.audio_download_btn = QPushButton("⬇️  Download Audio")
        self.audio_download_btn.setObjectName("PrimaryBtn")

        row.addWidget(self.audio_format_combo, 1)
        row.addWidget(self.audio_quality_combo, 2)
        row.addWidget(self.audio_download_btn, 1)

        card = self.card(row)

        hint = QLabel("Audio mode: Downloads best audio. MP3 conversion needs FFmpeg installed.")
        hint.setObjectName("Hint")

        layout.addWidget(card)
        layout.addWidget(hint)
        layout.addStretch(1)

        page = QFrame()
        page.setLayout(layout)

        self.audio_download_btn.clicked.connect(self.download_audio)

        return page

    def switch_page(self, index: int):
        self.pages.setCurrentIndex(index)
        self.fade_in_widget(self.pages.currentWidget())


        if index == 0:
            self.btn_video_mode.setProperty("active", True)
            self.btn_audio_mode.setProperty("active", False)
        else:
            self.btn_video_mode.setProperty("active", False)
            self.btn_audio_mode.setProperty("active", True)


        self.btn_video_mode.style().unpolish(self.btn_video_mode)
        self.btn_video_mode.style().polish(self.btn_video_mode)
        self.btn_audio_mode.style().unpolish(self.btn_audio_mode)
        self.btn_audio_mode.style().polish(self.btn_audio_mode)

    def apply_style(self):

        font = QFont("Segoe UI")
        font.setPointSize(10)
        QApplication.instance().setFont(font)

        self.setStyleSheet("""
        QWidget {
            background-color: #0b1220;
            color: #e5e7eb;
        }

        #Card {
            background: rgba(17, 24, 39, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 22px;
        }

        #Brand {
            font-size: 24px;
            font-weight: 800;
            padding: 4px 0;
            color: #ffffff;
        }

        #Tagline {
            font-size: 12px;
            color: rgba(226, 232, 240, 0.75);
            padding-bottom: 6px;
        }

        #HelpBox {
            font-size: 12px;
            color: rgba(226, 232, 240, 0.75);
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 16px;
            padding: 12px;
            line-height: 1.4;
        }

        #HeroTitle {
            font-size: 34px;
            font-weight: 900;
            letter-spacing: 0.3px;
            color: white;
        }

        #HeroSub {
            font-size: 12px;
            color: rgba(226, 232, 240, 0.75);
        }

        QLineEdit {
            background: rgba(30, 41, 59, 0.75);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 16px;
            padding: 12px 14px;
            font-size: 13px;
        }
        QLineEdit:focus {
            border: 1px solid rgba(59, 130, 246, 0.9);
        }

        QComboBox {
            background: rgba(30, 41, 59, 0.75);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 14px;
            padding: 10px 12px;
            font-size: 13px;
        }
        QComboBox::drop-down {
            border: none;
            width: 24px;
        }

        QPushButton {
            border-radius: 16px;
            padding: 11px 14px;
            font-weight: 700;
            border: 1px solid rgba(148, 163, 184, 0.18);
            background: rgba(30, 41, 59, 0.75);
        }
        QPushButton:hover {
            border: 1px solid rgba(59, 130, 246, 0.9);
            background: rgba(30, 41, 59, 0.95);
        }
        QPushButton:pressed {
            background: rgba(15, 23, 42, 0.95);
        }

        QPushButton#PrimaryBtn {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(59, 130, 246, 0.95),
                stop:1 rgba(147, 51, 234, 0.95)
            );
            border: none;
        }
        QPushButton#PrimaryBtn:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(59, 130, 246, 1.0),
                stop:1 rgba(236, 72, 153, 1.0)
            );
        }

        QPushButton#GhostBtn {
            background: rgba(30, 41, 59, 0.55);
        }

        QPushButton#SideBtn {
            text-align: left;
            padding: 12px 14px;
            border-radius: 16px;
            background: rgba(30, 41, 59, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.14);
        }
        QPushButton#SideBtn[active="true"] {
            background: rgba(59, 130, 246, 0.22);
            border: 1px solid rgba(59, 130, 246, 0.65);
        }

        #ThumbWrap {
            background: rgba(2, 6, 23, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 24px;
        }

        #ThumbLabel {
            background: rgba(30, 41, 59, 0.35);
            border: 1px dashed rgba(148, 163, 184, 0.25);
            border-radius: 18px;
            color: rgba(226, 232, 240, 0.7);
        }

        #VideoTitle {
            font-size: 18px;
            font-weight: 800;
            color: white;
        }

        #Hint {
            margin-left: 8px;
            margin-right: 8px;
            padding: 0px 6px;
            font-size: 12px;
            color: rgba(226, 232, 240, 0.7);
        }

        #Progress {
            background: rgba(30, 41, 59, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 12px;
            height: 16px;
        }
        #Progress::chunk {
            border-radius: 12px;
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(59, 130, 246, 1.0),
                stop:1 rgba(236, 72, 153, 1.0)
            );
        }

        #Status {
            font-size: 12px;
            color: rgba(226, 232, 240, 0.78);
        }
        """)

        self.btn_video_mode.setProperty("active", True)
        self.btn_audio_mode.setProperty("active", False)
        self.switch_page(0)


    def set_status(self, text: str):
        self.status_label.setText(text)

    def fetch_video(self):
        url = self.url_input.text().strip()
        if not url:
            self.set_status("Paste a link first.")
            return

        self.current_url = url
        self.set_status("Fetching video info…")
        self.progress_bar.setValue(0)

        try:
            with YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
                info = ydl.extract_info(url, download=False)

            title = info.get("title", "")
            self.title_label.setText(title if title else "Unknown title")

            self.thumbnail_url = info.get("thumbnail")
            if self.thumbnail_url:
                response = requests.get(self.thumbnail_url, timeout=15)
                response.raise_for_status()

                img = Image.open(BytesIO(response.content)).convert("RGB")
                img = img.resize((400, 225))

                data = BytesIO()
                img.save(data, format="PNG")
                pixmap = QPixmap()
                pixmap.loadFromData(data.getvalue())

                self.thumbnail_label.setPixmap(pixmap)
                self.thumbnail_label.setScaledContents(True)
                self.thumbnail_btn.show()

            self.build_formats(info)
            self.set_status("Ready ✨ Choose options and download.")

        except Exception as e:
            self.set_status(f"Error: {e}")

    def build_formats(self, info):
        self.video_formats = {}
        self.audio_formats = {}

        for f in info.get("formats", []):
            # Video formats
            if f.get("vcodec") != "none" and f.get("height"):
                ext = f.get("ext")
                height = f.get("height")
                fps = f.get("fps")
                label = f"{height}p" + (f" {int(fps)}fps" if fps else "")

                key = (ext, label)
                if key not in self.video_formats:
                    self.video_formats[key] = f
                else:
                    old = self.video_formats[key]
                    if (f.get("tbr") or 0) > (old.get("tbr") or 0):
                        self.video_formats[key] = f

            # Audio formats
            if f.get("vcodec") == "none" and f.get("acodec") != "none":
                ext = f.get("ext")
                abr = f.get("abr")
                if abr:
                    label = f"{int(abr)}k"
                    key = (ext, label)
                    if key not in self.audio_formats:
                        self.audio_formats[key] = f
                    else:
                        old = self.audio_formats[key]
                        if (f.get("abr") or 0) > (old.get("abr") or 0):
                            self.audio_formats[key] = f

        self.update_video_resolutions()

    def update_video_resolutions(self):
        ext = self.video_format_combo.currentText()
        resolutions = [r for (e, r) in self.video_formats.keys() if e == ext]

        def height_key(r):
            try:
                return int(r.split("p")[0])
            except:
                return 0

        resolutions.sort(key=height_key, reverse=True)

        self.resolution_combo.clear()
        if resolutions:
            self.resolution_combo.addItems(resolutions)
        else:
            self.resolution_combo.addItem("No formats found")

    def clear_all(self):
        self.current_url = None
        self.thumbnail_url = None
        self.video_formats = {}
        self.audio_formats = {}

        self.url_input.clear()
        self.thumbnail_label.setText("Thumbnail preview")
        self.thumbnail_label.setPixmap(QPixmap())
        self.thumbnail_label.setScaledContents(False)
        self.title_label.setText("Paste a link and Fetch ✨")
        self.thumbnail_btn.hide()
        self.progress_bar.setValue(0)
        self.set_status("Ready.")

        self.resolution_combo.clear()

    def cancel_download(self):
        if self.thread and self.thread.isRunning():
            self.thread.cancel()
            self.set_status("Cancelling…")

    def download_thumbnail(self):
        if not self.thumbnail_url:
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Thumbnail", "", "JPEG Image (*.jpg)"
        )
        if not save_path:
            return

        try:
            response = requests.get(self.thumbnail_url, timeout=15)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)
            self.set_status("Thumbnail saved ✅")
        except Exception as e:
            self.set_status(f"Error saving thumbnail: {e}")

    def download_video(self):
        if not self.current_url:
            self.set_status("Fetch a video first.")
            return

        ext = self.video_format_combo.currentText()
        res = self.resolution_combo.currentText()
        key = (ext, res)

        if key not in self.video_formats:
            self.set_status("That resolution isn’t available.")
            return

        format_id = self.video_formats[key]["format_id"]

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Video", "", f"{ext.upper()} files (*.{ext})"
        )
        if not save_path:
            return

        ydl_opts = {
            "format": f"{format_id}+bestaudio/best",
            "outtmpl": save_path,
            "merge_output_format": ext,
            "noprogress": True,  
        }

        self.start_download(ydl_opts)

    def download_audio(self):
        if not self.current_url:
            self.set_status("Fetch a video first.")
            return

        ext = self.audio_format_combo.currentText()

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Audio", "", f"{ext.upper()} files (*.{ext})"
        )
        if not save_path:
            return

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": save_path,
            "noprogress": True,
        }


        if ext == "mp3":
            q = self.audio_quality_combo.currentText()
            preferred = "192"
            if q == "320k":
                preferred = "320"
            elif q == "192k":
                preferred = "192"
            elif q == "128k":
                preferred = "128"
            else:
                preferred = "192"

            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": preferred,
            }]

        self.start_download(ydl_opts)

    def start_download(self, ydl_opts):
        if self.thread and self.thread.isRunning():
            self.set_status("A download is already running.")
            return

        self.progress_bar.setValue(0)
        self.set_status("Starting…")

        self.thread = DownloadThread(self.current_url, ydl_opts)
        self.thread.progress_text.connect(self.set_status)
        self.thread.progress_value.connect(self.progress_bar.setValue)
        self.thread.finished_signal.connect(self.on_download_finished)
        self.thread.start()

    def on_download_finished(self, msg):
        self.set_status(msg)
        if "complete" in msg.lower():
            self.progress_bar.setValue(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = QWidget()
    splash.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    splash.setAttribute(Qt.WA_TranslucentBackground)
    splash.setWindowOpacity(0.0)

    layout = QVBoxLayout(splash)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)

    splash_pix = QPixmap(resource_path("splash.png"))
    image_label = QLabel()
    image_label.setPixmap(splash_pix)
    image_label.setAlignment(Qt.AlignCenter)

    layout.addWidget(image_label)

    progress = QProgressBar()
    progress.setRange(0, 100)
    progress.setValue(0)
    progress.setFixedHeight(28)  
    progress.setTextVisible(False)

    progress.setStyleSheet("""
        QProgressBar {
            background: rgba(255,255,255,0.08);
            border-radius: 14px;
        }

        QProgressBar::chunk {
            border-radius: 14px;
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #ff512f,
                stop:1 #dd2476


            );
        }
    """)

    layout.addWidget(progress)

    splash.adjustSize()
    splash.show()
    splash.move(
        app.primaryScreen().geometry().center() - splash.rect().center()
    )

    app.processEvents()

    fade_in = QPropertyAnimation(splash, b"windowOpacity")
    fade_in.setDuration(600)
    fade_in.setStartValue(0.0)
    fade_in.setEndValue(1.0)
    fade_in.start()

    progress_anim = QPropertyAnimation(progress, b"value")
    progress_anim.setDuration(3000)
    progress_anim.setStartValue(0)
    progress_anim.setEndValue(100)
    progress_anim.start()

    def start_main_window():
        window = YouTubeDownloader()
        window.setWindowOpacity(0.0)
        window.show()

        fade_out = QPropertyAnimation(splash, b"windowOpacity")
        fade_out.setDuration(600)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)

        def finish_transition():
            splash.close()

            fade_window = QPropertyAnimation(window, b"windowOpacity")
            fade_window.setDuration(600)
            fade_window.setStartValue(0.0)
            fade_window.setEndValue(1.0)
            fade_window.start()

            window._fade_anim = fade_window

        fade_out.finished.connect(finish_transition)
        fade_out.start()

        splash._fade_anim = fade_out

    QTimer.singleShot(3000, start_main_window)

    sys.exit(app.exec_())
