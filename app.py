import os
import sys

from PySide6.QtWidgets import QApplication

from ui.media_app import MediaApp
from ui.splash_screen import SplashScreen

# testing out discord commit message webhook integration.

os.environ["PATH"] += os.pathsep + "ffmpeg"

if __name__ == "__main__":
  app = QApplication(sys.argv)
  splash = SplashScreen()
  window = MediaApp()

  splash.finished.connect(window.show)
  splash.start_animation()

  sys.exit(app.exec())
