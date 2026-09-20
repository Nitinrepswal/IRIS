from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton
)

from PySide6.QtCore import (
    QThread,
    Signal
)

from app.worker import IRISWorker


class ChatWidget(QWidget):
    process_message = Signal(str)

    def __init__(self):
        super().__init__()

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Ask IRIS anything..."
        )

        self.send_button = QPushButton(
            "Send"
        )

        self.send_button.clicked.connect(
            self.send_message
        )

        self.input.returnPressed.connect(
            self.send_message
        )

        input_layout = QHBoxLayout()

        input_layout.addWidget(
            self.input
        )

        input_layout.addWidget(
            self.send_button
        )

        layout = QVBoxLayout()

        layout.addWidget(
            self.chat
        )

        layout.addLayout(
            input_layout
        )

        self.setLayout(layout)

        self.thread = QThread()

        self.worker = IRISWorker()

        self.worker.moveToThread(
            self.thread
        )

        self.process_message.connect(
            self.worker.process
        )

        self.worker.finished.connect(
            self.handle_response
        )

        self.worker.error.connect(
            self.handle_error
        )

        self.thread.start()

    def send_message(self):
        message = self.input.text().strip()

        if not message:
            return

        self.chat.append(
            f"<b>You:</b> {message}"
        )

        self.input.clear()

        self.send_button.setEnabled(
            False
        )

        self.input.setEnabled(
            False
        )

        self.chat.append(
            "<i>IRIS is thinking...</i>"
        )

        self.process_message.emit(
            message
        )

    def handle_response(self, response):
        document = self.chat.document()

        cursor = self.chat.textCursor()

        cursor.movePosition(
            cursor.MoveOperation.End
        )

        block = cursor.block()

        if (
            "IRIS is thinking..."
            in block.text()
        ):
            cursor.select(
                cursor.SelectionType.BlockUnderCursor
            )

            cursor.removeSelectedText()

            self.chat.setTextCursor(
                cursor
            )

        self.chat.append(
            f"<b>IRIS:</b> {response}"
        )

        self.send_button.setEnabled(
            True
        )

        self.input.setEnabled(
            True
        )

        self.input.setFocus()

    def handle_error(self, error):
        self.chat.append(
            f"<b>IRIS:</b> Error: {error}"
        )

        self.send_button.setEnabled(
            True
        )

        self.input.setEnabled(
            True
        )

        self.input.setFocus()

    def closeEvent(self, event):
        self.thread.quit()
        self.thread.wait()

        event.accept()