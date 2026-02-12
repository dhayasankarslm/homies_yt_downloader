import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import YouTubeDownloader
from ui.splash_screen import SplashScreen

if __name__ == "__main__":
  app = QApplication(sys.argv)
  splash = SplashScreen()
  window = YouTubeDownloader()

  splash.finished.connect(window.show)
  splash.start_animation()

  sys.exit(app.exec())
