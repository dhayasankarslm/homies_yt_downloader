def get_stylesheet():
  return """
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
    """
