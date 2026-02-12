import os
import sys


def resource_path(relative_path: str):
  if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    base_path = sys._MEIPASS
  else:
    # Assuming this file is in utils/, so we go up one level to root
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  return os.path.join(base_path, relative_path)
