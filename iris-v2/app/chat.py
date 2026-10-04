from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QLabel,
    QFrame,
    QScrollArea
)

from PySide6.QtCore import (
    QThread,
    Signal,
    Qt
)

from app.worker import (
    IRISWorker,
    VoiceWorker,
    SpeechWorker
)


class ChatWidget(QWidget):
    process_message = Signal(str)
    start_voice = Signal()
    stop_voice = Signal()
    stop_speech = Signal()
    speak_response = Signal(str)
    execute_approved = Signal(str)

    def __init__(self):
        super().__init__()

        self.closing = False
        self.audio_enabled = True
        self.thinking_widget = None

        self.create_chat_area()
        self.create_composer()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addWidget(
            self.scroll_area,
            1
        )

        layout.addWidget(
            self.composer
        )

        self.setLayout(layout)

        self.create_workers()

        self.add_message(
            "IRIS",
            "Hello! I'm IRIS. 👋\n"
            "Your personal AI assistant. "
            "How can I help you today?"
        )

    def create_chat_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)

        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: #0F1117;
                border: none;
            }

            QScrollArea > QWidget {
                background: #0F1117;
            }

            QScrollBar:vertical {
                background: #0F1117;
                width: 7px;
                margin: 4px 2px;
            }

            QScrollBar::handle:vertical {
                background: #303747;
                border-radius: 4px;
                min-height: 35px;
            }

            QScrollBar::handle:vertical:hover {
                background: #475569;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

        self.chat_container = QWidget()
        self.chat_container.setStyleSheet(
            "background: #0F1117;"
        )

        self.chat_layout = QVBoxLayout()

        self.chat_layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        self.chat_layout.setSpacing(20)

        self.chat_layout.addStretch()

        self.chat_container.setLayout(
            self.chat_layout
        )

        self.scroll_area.setWidget(
            self.chat_container
        )

    def create_composer(self):
        self.composer = QFrame()
        self.composer.setObjectName("composer")

        layout = QHBoxLayout()

        layout.setContentsMargins(
            7,
            7,
            7,
            7
        )

        layout.setSpacing(6)

        self.attach_button = QPushButton("+")
        self.attach_button.setObjectName(
            "composerSecondary"
        )
        self.attach_button.setFixedSize(
            42,
            42
        )

        self.input = QLineEdit()
        self.input.setPlaceholderText(
            "Ask IRIS anything..."
        )

        self.voice_button = QPushButton("🎙")
        self.voice_button.setObjectName(
            "composerSecondary"
        )
        self.voice_button.setFixedSize(
            46,
            42
        )
        self.voice_button.setToolTip(
            "Talk to IRIS"
        )

        self.audio_button = QPushButton("🔊")
        self.audio_button.setObjectName(
            "composerSecondary"
        )
        self.audio_button.setFixedSize(
            46,
            42
        )
        self.audio_button.setToolTip(
            "Audio response: ON"
        )

        self.send_button = QPushButton("➤")
        self.send_button.setObjectName(
            "sendButton"
        )
        self.send_button.setFixedSize(
            46,
            42
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

        self.audio_button.clicked.connect(
            self.toggle_audio
        )

        layout.addWidget(
            self.attach_button
        )

        layout.addWidget(
            self.input,
            1
        )

        layout.addWidget(
            self.voice_button
        )

        layout.addWidget(
            self.audio_button
        )

        layout.addWidget(
            self.send_button
        )

        self.composer.setLayout(layout)

    def create_workers(self):
        self.thread = QThread()
        self.worker = IRISWorker()

        self.worker.moveToThread(
            self.thread
        )

        self.process_message.connect(
            self.worker.process
        )

        self.execute_approved.connect(
            self.worker.execute_message
        )

        self.worker.finished.connect(
            self.handle_response
        )

        self.worker.error.connect(
            self.handle_error
        )

        self.worker.permission_required.connect(
            self.handle_permission_request
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

        self.stop_voice.connect(
            self.voice_worker.stop
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

        self.stop_speech.connect(
            self.speech_worker.stop
        )

        self.speech_worker.error.connect(
            self.handle_speech_error
        )

        self.speech_thread.start()

    def add_message(self, sender, message):
        row = QWidget()
        row.setStyleSheet(
            "background: transparent;"
        )

        row_layout = QHBoxLayout()

        row_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        row_layout.setSpacing(9)

        bubble = QFrame()
        bubble.setMaximumWidth(720)

        bubble_layout = QVBoxLayout()

        bubble_layout.setContentsMargins(
            15,
            11,
            15,
            11
        )

        bubble_layout.setSpacing(3)

        sender_label = QLabel(sender)
        sender_label.setObjectName(
            "messageSender"
        )

        message_label = QLabel(message)
        message_label.setObjectName(
            "messageText"
        )

        message_label.setWordWrap(True)

        message_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        bubble_layout.addWidget(
            sender_label
        )

        bubble_layout.addWidget(
            message_label
        )

        bubble.setLayout(
            bubble_layout
        )

        if sender == "You":
            bubble.setObjectName(
                "userBubble"
            )

            avatar = QFrame()
            avatar.setObjectName(
                "userAvatar"
            )

            avatar.setFixedSize(
                32,
                32
            )

            avatar_layout = QVBoxLayout()
            avatar_layout.setContentsMargins(
                0,
                0,
                0,
                0
            )

            avatar_text = QLabel("●")
            avatar_text.setObjectName(
                "userAvatarText"
            )

            avatar_text.setAlignment(
                Qt.AlignCenter
            )

            avatar_layout.addWidget(
                avatar_text
            )

            avatar.setLayout(
                avatar_layout
            )

            row_layout.addStretch()

            row_layout.addWidget(
                bubble
            )

            row_layout.addWidget(
                avatar,
                alignment=Qt.AlignBottom
            )

        else:
            bubble.setObjectName(
                "irisBubble"
            )

            avatar = QFrame()
            avatar.setObjectName(
                "avatar"
            )

            avatar.setFixedSize(
                32,
                32
            )

            avatar_layout = QVBoxLayout()
            avatar_layout.setContentsMargins(
                0,
                0,
                0,
                0
            )

            avatar_text = QLabel("✦")
            avatar_text.setObjectName(
                "avatarText"
            )

            avatar_text.setAlignment(
                Qt.AlignCenter
            )

            avatar_layout.addWidget(
                avatar_text
            )

            avatar.setLayout(
                avatar_layout
            )

            row_layout.addWidget(
                avatar,
                alignment=Qt.AlignBottom
            )

            row_layout.addWidget(
                bubble
            )

            row_layout.addStretch()

        row.setLayout(
            row_layout
        )

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            row
        )

        self.scroll_to_bottom()

    def add_thinking(
        self,
        text="IRIS is thinking..."
    ):
        self.remove_thinking()

        row = QWidget()

        row_layout = QHBoxLayout()

        row_layout.setContentsMargins(
            42,
            0,
            0,
            0
        )

        label = QLabel(text)
        label.setObjectName(
            "thinking"
        )

        row_layout.addWidget(label)
        row_layout.addStretch()

        row.setLayout(
            row_layout
        )

        self.thinking_widget = row

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            row
        )

        self.scroll_to_bottom()

    def remove_thinking(self):
        if self.thinking_widget is None:
            return

        widget = self.thinking_widget

        self.chat_layout.removeWidget(
            widget
        )

        widget.deleteLater()

        self.thinking_widget = None

    def scroll_to_bottom(self):
        scrollbar = (
            self.scroll_area.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )

    def toggle_audio(self):
        self.audio_enabled = (
            not self.audio_enabled
        )

        if self.audio_enabled:
            self.audio_button.setText(
                "🔊"
            )

            self.audio_button.setToolTip(
                "Audio response: ON"
            )

        else:
            self.audio_button.setText(
                "🔇"
            )

            self.audio_button.setToolTip(
                "Audio response: OFF"
            )

            self.stop_speech.emit()

    def send_message(self):
        if self.closing:
            return

        message = self.input.text().strip()

        if not message:
            return

        self.add_message(
            "You",
            message
        )

        self.input.clear()

        self.send_button.setEnabled(False)
        self.voice_button.setEnabled(False)
        self.input.setEnabled(False)

        self.add_thinking()

        self.process_message.emit(
            message
        )

    def start_voice_input(self):
        if self.closing:
            return

        self.voice_button.setEnabled(False)
        self.send_button.setEnabled(False)
        self.input.setEnabled(False)

        self.add_thinking(
            "IRIS is listening..."
        )

        self.start_voice.emit()

    def handle_voice_result(self, text):
        if self.closing:
            return

        self.remove_thinking()

        if not text:
            self.add_message(
                "IRIS",
                "I didn't hear anything."
            )

            self.voice_button.setEnabled(True)
            self.send_button.setEnabled(True)
            self.input.setEnabled(True)
            self.input.setFocus()

            return

        self.add_message(
            "You",
            text
        )

        self.add_thinking()

        self.process_message.emit(
            text
        )

    def handle_voice_error(self, error):
        if self.closing:
            return

        self.remove_thinking()

        self.add_message(
            "IRIS",
            f"Voice error: {error}"
        )

        self.voice_button.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input.setEnabled(True)
        self.input.setFocus()

    def handle_permission_request(
        self,
        action,
        message
    ):
        if self.closing:
            return

        box = QMessageBox(self)

        box.setWindowTitle(
            "IRIS Permission Request"
        )

        box.setText(
            f"IRIS wants to perform "
            f"'{action}'."
        )

        box.setInformativeText(
            f"Request:\n{message}\n\n"
            "Allow this action?"
        )

        allow = box.addButton(
            "Allow",
            QMessageBox.AcceptRole
        )

        box.addButton(
            "Deny",
            QMessageBox.RejectRole
        )

        box.exec()

        if box.clickedButton() == allow:
            self.add_message(
                "IRIS",
                "Permission granted."
            )

            self.execute_approved.emit(
                message
            )

        else:
            self.add_message(
                "IRIS",
                "Permission denied."
            )

            self.handle_response(
                "I did not perform that action."
            )

    def handle_response(self, response):
        if self.closing:
            return

        self.remove_thinking()

        self.add_message(
            "IRIS",
            response
        )

        if self.audio_enabled:
            self.speak_response.emit(
                response
            )

        self.send_button.setEnabled(True)
        self.voice_button.setEnabled(True)
        self.input.setEnabled(True)
        self.input.setFocus()

    def handle_error(self, error):
        if self.closing:
            return

        self.remove_thinking()

        self.add_message(
            "IRIS",
            f"Error: {error}"
        )

        self.send_button.setEnabled(True)
        self.voice_button.setEnabled(True)
        self.input.setEnabled(True)
        self.input.setFocus()

    def handle_speech_error(self, error):
        if self.closing:
            return

        self.add_message(
            "IRIS",
            f"Voice output error: {error}"
        )

    def closeEvent(self, event):
        self.closing = True

        self.send_button.setEnabled(False)
        self.voice_button.setEnabled(False)
        self.input.setEnabled(False)

        self.stop_voice.emit()
        self.stop_speech.emit()

        self.thread.quit()
        self.voice_thread.quit()
        self.speech_thread.quit()

        event.accept()