from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect


def apply_shadow(widget, blur=35, x=0, y=12, opacity=120):
  shadow = QGraphicsDropShadowEffect(widget)
  shadow.setBlurRadius(blur)
  shadow.setOffset(x, y)
  shadow.setColor(QColor(0, 0, 0, opacity))
  widget.setGraphicsEffect(shadow)


def create_card(layout=None):
  frame = QFrame()
  frame.setObjectName("Card")
  if layout:
    frame.setLayout(layout)
  apply_shadow(frame)
  return frame
