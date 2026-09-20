from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton
)


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText(
            "Ask IRIS anything..."
        )

        self.send_button = QPushButton("Send")

        self.send_button.clicked.connect(
            self.send_message
        )

        self.input.returnPressed.connect(
            self.send_message
        )

        input_layout = QHBoxLayout()

        input_layout.addWidget(self.input)
        input_layout.addWidget(
            self.send_button
        )

        layout = QVBoxLayout()

        layout.addWidget(self.chat)
        layout.addLayout(input_layout)

        self.setLayout(layout)

    def send_message(self):
        message = self.input.text().strip()

        if not message:
            return

        self.chat.append(
            f"<b>You:</b> {message}"
        )

        self.chat.append(
            "<b>IRIS:</b> I'm ready to help."
        )

        self.input.clear()
        self.input.setFocus()