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

from app.worker import (
    IRISWorker,
    VoiceWorker,
    SpeechWorker
)


class ChatWidget(QWidget):
    process_message = Signal(str)
    start_voice = Signal()
    speak_response = Signal(str)

    def __init__(self):
        super().__init__()

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText(
            "Ask IRIS anything..."
        )

        self.send_button = QPushButton("Send")
        self.send_button.setToolTip(
            "Send message"
        )

        self.voice_button = QPushButton("🎙️")
        self.voice_button.setToolTip(
            "Talk to IRIS"
        )

        self.send_button.clicked.connect(
            self.send_message
        )

        self.input.returnPressed.connect(
            self.send_message
        )

        self.voice_button.clicked.connect(
            self.start_voice_input
        )

        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        input_layout.addWidget(self.input)
        input_layout.addWidget(
            self.voice_button
        )
        input_layout.addWidget(
            self.send_button
        )

        layout = QVBoxLayout()
        layout.setSpacing(10)

        layout.addWidget(self.chat)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        self.chat.append(
            "<b>IRIS:</b> Hello! I'm IRIS. "
            "How can I help you?"
        )

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

        self.voice_thread = QThread()
        self.voice_worker = VoiceWorker()

        self.voice_worker.moveToThread(
            self.voice_thread
        )

        self.start_voice.connect(
            self.voice_worker.listen
        )

        self.voice_worker.finished.connect(
            self.handle_voice_result
        )

        self.voice_worker.error.connect(
            self.handle_voice_error
        )

        self.voice_thread.start()

        self.speech_thread = QThread()
        self.speech_worker = SpeechWorker()

        self.speech_worker.moveToThread(
            self.speech_thread
        )

        self.speak_response.connect(
            self.speech_worker.speak
        )

        self.speech_worker.error.connect(
            self.handle_speech_error
        )

        self.speech_thread.start()

    def send_message(self):
        message = self.input.text().strip()

        if not message:
            return

        self.chat.append(
            f"<b>You:</b> {message}"
        )

        self.input.clear()

        self.send_button.setEnabled(False)
        self.voice_button.setEnabled(False)
        self.input.setEnabled(False)

        self.chat.append(
            "<i>IRIS is thinking...</i>"
        )

        self.process_message.emit(
            message
        )

    def start_voice_input(self):
        self.voice_button.setEnabled(False)
        self.send_button.setEnabled(False)
        self.input.setEnabled(False)

        self.chat.append(
            "<i>IRIS is listening...</i>"
        )

        self.start_voice.emit()

    def handle_voice_result(self, text):
        if not text:
            self.chat.append(
                "<i>No speech detected.</i>"
            )

            self.voice_button.setEnabled(True)
            self.send_button.setEnabled(True)
            self.input.setEnabled(True)
            self.input.setFocus()

            return

        self.input.setText(text)

        self.chat.append(
            f"<b>You:</b> {text}"
        )

        self.chat.append(
            "<i>IRIS is thinking...</i>"
        )

        self.process_message.emit(text)

    def handle_voice_error(self, error):
        self.chat.append(
            f"<b>IRIS:</b> Voice error: {error}"
        )

        self.voice_button.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input.setEnabled(True)
        self.input.setFocus()

    def handle_response(self, response):
        cursor = self.chat.textCursor()

        cursor.movePosition(
            cursor.MoveOperation.End
        )

        block = cursor.block()

        if "IRIS is thinking..." in block.text():
            cursor.select(
                cursor.SelectionType.BlockUnderCursor
            )

            cursor.removeSelectedText()

            self.chat.setTextCursor(cursor)

        self.chat.append(
            f"<b>IRIS:</b> {response}"
        )

        self.speak_response.emit(
            response
        )

        self.send_button.setEnabled(True)
        self.voice_button.setEnabled(True)
        self.input.setEnabled(True)
        self.input.setFocus()

    def handle_error(self, error):
        self.chat.append(
            f"<b>IRIS:</b> Error: {error}"
        )

        self.send_button.setEnabled(True)
        self.voice_button.setEnabled(True)
        self.input.setEnabled(True)
        self.input.setFocus()

    def handle_speech_error(self, error):
        self.chat.append(
            f"<b>IRIS:</b> Voice output error: {error}"
        )

    def closeEvent(self, event):
        self.thread.quit()
        self.thread.wait()

        self.voice_thread.quit()
        self.voice_thread.wait()

        self.speech_thread.quit()
        self.speech_thread.wait()

        event.accept()