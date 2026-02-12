from PySide6.QtCore import QThread, Signal
from yt_dlp import YoutubeDL


class DownloadThread(QThread):
  progress_text = Signal(str)
  progress_value = Signal(int)
  finished_signal = Signal(str)

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
            speed_txt = f" • {speed / 1024 / 1024:.2f} MB/s"
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
