from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget
)
from PySide6.QtCore import Qt


class IRISWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IRIS")
        self.resize(900, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("IRIS")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "Your AI assistant"
        )
        subtitle.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

        central_widget.setLayout(layout)

        self.setCentralWidget(
            central_widget
        )