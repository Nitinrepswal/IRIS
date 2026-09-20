from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt

from app.chat import ChatWidget


class IRISWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IRIS")
        self.resize(900, 600)

        central_widget = QWidget()

        layout = QVBoxLayout()

        title = QLabel("IRIS")
        title.setAlignment(
            Qt.AlignCenter
        )

        subtitle = QLabel(
            "Your AI assistant"
        )
        subtitle.setAlignment(
            Qt.AlignCenter
        )

        chat = ChatWidget()

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(chat)

        central_widget.setLayout(layout)

        self.setCentralWidget(
            central_widget
        )