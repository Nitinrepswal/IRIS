from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from app.chat import ChatWidget


class IRISWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IRIS V2.2")
        self.resize(1000, 700)
        self.setMinimumSize(800, 550)

        central_widget = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(8)

        title = QLabel("IRIS")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        version = QLabel("V2.2")
        version.setAlignment(Qt.AlignCenter)
        version.setObjectName("version")

        subtitle = QLabel("Your AI assistant")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitle")

        status = QLabel("● Online")
        status.setAlignment(Qt.AlignCenter)
        status.setObjectName("status")

        chat = ChatWidget()

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(subtitle)
        layout.addWidget(status)
        layout.addSpacing(12)
        layout.addWidget(chat)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f1117;
            }

            QWidget {
                background-color: #0f1117;
                color: #ffffff;
                font-family: Arial;
            }

            QLabel#title {
                font-size: 32px;
                font-weight: bold;
            }

            QLabel#version {
                font-size: 14px;
                color: #888888;
            }

            QLabel#subtitle {
                font-size: 16px;
                color: #aaaaaa;
            }

            QLabel#status {
                font-size: 13px;
                color: #55cc88;
            }

            QTextEdit {
                background-color: #171a22;
                border: 1px solid #2a2e38;
                border-radius: 12px;
                padding: 12px;
                font-size: 14px;
            }

            QLineEdit {
                background-color: #171a22;
                border: 1px solid #2a2e38;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #222733;
                border: 1px solid #333947;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #2b3140;
            }

            QPushButton:pressed {
                background-color: #1c2029;
            }

            QPushButton:disabled {
                color: #666666;
            }
        """)