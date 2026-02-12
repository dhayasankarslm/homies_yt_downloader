import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import YouTubeDownloader
from ui.splash_screen import SplashScreen

if __name__ == "__main__":
  app = QApplication(sys.argv)
  splash = SplashScreen()
  window = YouTubeDownloader()


  def show_main_window():
    window.show()


  splash.finished.connect(show_main_window)
  splash.start_animation()

  sys.exit(app.exec())
