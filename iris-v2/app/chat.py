import os
import subprocess
from PySide6.QtWidgets import (
    QWidget,
    QInputDialog,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QLabel,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
)

from PySide6.QtCore import (
    QThread,
    Signal,
    Qt,
    QTimer,
    QSize,
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRadialGradient,
    QTextBlockFormat,
    QTextCursor,
    QTextDocument,
)

import re
from datetime import datetime
from uuid import uuid4

from app.worker import IRISWorker, VoiceWorker, SpeechWorker
from memory.conversation_store import ConversationStore
from memory.profile import PersonalProfile


def welcome_greeting(current_time=None, user_name=""):
    """Build a local-time greeting without requiring profile data."""
    hour = (current_time or datetime.now()).hour

    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return f"{greeting}, {user_name}." if user_name else greeting


def voice_icon(kind, muted=False):
    """Create scale-safe monochrome icons without platform-dependent glyphs."""
    size = 32
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QPen(QColor("#E4EAF2"), 2.4, Qt.PenStyle.SolidLine,
                        Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)

    if kind == "microphone":
        capsule = QPainterPath()
        capsule.addRoundedRect(11, 4, 10, 15, 5, 5)
        painter.drawPath(capsule)

        stem = QPainterPath()
        stem.moveTo(7, 15)
        stem.cubicTo(7, 23, 25, 23, 25, 15)
        painter.drawPath(stem)
        painter.drawLine(16, 23, 16, 28)
        painter.drawLine(11, 28, 21, 28)
    else:
        speaker = QPainterPath()
        speaker.moveTo(5, 13)
        speaker.lineTo(11, 13)
        speaker.lineTo(18, 7)
        speaker.lineTo(18, 25)
        speaker.lineTo(11, 19)
        speaker.lineTo(5, 19)
        speaker.closeSubpath()
        painter.drawPath(speaker)

        if muted:
            painter.drawLine(22, 12, 28, 20)
            painter.drawLine(28, 12, 22, 20)
        else:
            painter.drawArc(17, 10, 10, 12, -55 * 16, 110 * 16)
            painter.drawArc(17, 6, 15, 20, -55 * 16, 110 * 16)

    painter.end()
    return QIcon(pixmap)


def more_icon():
    """Create a font-independent three-dot menu icon."""
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#C8D3E0"))
    for position in (6, 12, 18):
        painter.drawEllipse(position - 2, 10, 4, 4)
    painter.end()
    return QIcon(pixmap)


class WelcomeBackdrop(QWidget):
    """Small, self-contained decorative treatment for the idle chat state."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(172)
        self.setMaximumHeight(172)

    def paintEvent(self, event):
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        center_x = width / 2
        center_y = 84

        for offset, color, width_pen in [
            (0, QColor(53, 139, 241, 115), 1.3),
            (20, QColor(39, 99, 177, 75), 1.0),
            (-20, QColor(33, 81, 147, 55), 1.0),
        ]:
            path = QPainterPath()
            path.moveTo(0, 112 + offset)
            path.cubicTo(
                width * 0.2,
                86 + offset,
                width * 0.34,
                132 + offset,
                center_x,
                110 + offset,
            )
            path.cubicTo(
                width * 0.66,
                86 + offset,
                width * 0.8,
                132 + offset,
                width,
                110 + offset,
            )
            painter.setPen(QPen(color, width_pen))
            painter.drawPath(path)

        glow = QRadialGradient(center_x, center_y, 74)
        glow.setColorAt(0, QColor(33, 111, 203, 95))
        glow.setColorAt(0.55, QColor(28, 75, 136, 35))
        glow.setColorAt(1, QColor(18, 24, 32, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(glow)
        painter.drawEllipse(int(center_x - 74), center_y - 74, 148, 148)

        badge = QRadialGradient(center_x - 14, center_y - 17, 92)
        badge.setColorAt(0, QColor(43, 109, 179, 235))
        badge.setColorAt(1, QColor(20, 52, 92, 245))
        painter.setBrush(badge)
        painter.drawEllipse(int(center_x - 57), center_y - 57, 114, 114)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(211, 231, 252), 4))
        painter.drawEllipse(int(center_x - 25), center_y - 25, 50, 50)
        painter.setPen(QPen(QColor(109, 183, 255), 2))
        painter.drawEllipse(int(center_x - 33), center_y - 33, 66, 66)


class ChatWidget(QWidget):
    process_message = Signal(str)
    start_voice = Signal()
    stop_voice = Signal()
    stop_speech = Signal()
    speak_response = Signal(str)
    execute_approved = Signal(str)
    conversations_changed = Signal()
    conversation_error = Signal(str)

    def __init__(self, conversation_store=None):
        super().__init__()

        self.closing = False
        self.audio_enabled = True
        self.thinking_widget = None
        self.last_user_message = ""
        self.active_request = None
        self.is_busy = False
        self.message_bubbles = []
        self.regenerate_buttons = []
        self.conversation_store = conversation_store or ConversationStore()
        self.conversations = self.conversation_store.load_document()[
            "conversations"
        ]
        self.active_conversation_id = None
        self.active_request_conversation_id = None
        self.discard_pending_response = False

        self.setObjectName("chatWidget")

        self.create_header()
        self.create_chat_area()
        self.create_composer()
        self.create_workers()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.header)
        layout.addWidget(self.chat_stack, 1)
        composer_container = QWidget()
        composer_layout = QVBoxLayout(composer_container)
        composer_layout.setContentsMargins(12, 0, 12, 12)
        composer_layout.addWidget(self.composer)
        layout.addWidget(composer_container)

        self.apply_styles()

    def create_header(self):
        self.header = QFrame()
        self.header.setObjectName("chatHeader")

        layout = QHBoxLayout(self.header)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(10)

        avatar = QLabel("◎")
        avatar.setObjectName("headerAvatar")
        avatar.setFixedSize(44, 44)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        identity = QVBoxLayout()
        identity.setSpacing(3)

        title = QLabel("IRIS")
        title.setObjectName("headerTitle")

        subtitle = QLabel("Personal AI assistant")
        subtitle.setObjectName("headerSubtitle")

        identity.addWidget(title)
        identity.addWidget(subtitle)

        layout.addWidget(avatar)
        layout.addLayout(identity)
        layout.addStretch()

        self.audio_status = QLabel("Voice on")
        self.audio_status.setObjectName("audioStatus")
        layout.addWidget(self.audio_status)

        self.header_audio_button = QPushButton()
        self.header_audio_button.setObjectName("iconButton")
        self.header_audio_button.setFixedSize(48, 48)
        self.header_audio_button.setIcon(voice_icon("speaker"))
        self.header_audio_button.setIconSize(QSize(22, 22))
        self.header_audio_button.setToolTip("Toggle voice responses")
        self.header_audio_button.setAccessibleName("Voice responses")
        self.header_audio_button.clicked.connect(self.toggle_audio)

        layout.addWidget(self.header_audio_button)

    def create_chat_area(self):
        self.chat_stack = QStackedWidget()
        self.chat_stack.setObjectName("chatStack")

        self.welcome_page = self.create_welcome_page()
        self.chat_stack.addWidget(self.welcome_page)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("chatScroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.chat_container = QWidget()
        self.chat_container.setObjectName("chatContainer")

        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(20, 12, 20, 12)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()

        self.scroll_area.setWidget(self.chat_container)
        self.chat_stack.addWidget(self.scroll_area)

        self.chat_stack.setCurrentWidget(self.welcome_page)

    def create_welcome_page(self):
        page = QWidget()
        page.setObjectName("welcomePage")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 12, 24, 10)
        layout.setSpacing(0)

        layout.addStretch(1)

        hero = QWidget()
        hero.setObjectName("welcomeHero")
        hero.setMaximumWidth(760)

        center = QVBoxLayout(hero)
        center.setContentsMargins(0, 0, 0, 0)
        center.setSpacing(7)

        visual = WelcomeBackdrop()

        profile_name = PersonalProfile().get_name().strip() or "Nitin"
        heading = QLabel(welcome_greeting(user_name=profile_name))
        heading.setObjectName("welcomeTitle")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel(
            "Welcome back. What can I help you with?"
        )
        subtitle.setObjectName("welcomeSubtitle")
        subtitle.setMaximumWidth(520)
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        center.addWidget(visual)
        center.addSpacing(2)
        center.addWidget(heading)
        center.addWidget(subtitle)

        layout.addWidget(hero, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(16)

        prompts = [
            ("⌕", "Search the web", "Find current information and sources.", "Search web for "),
            ("▤", "Find a file", "Search files available on your Mac.", "Find file "),
            ("⌘", "Open application ", "Launch an application on your Mac.", "Open Application"),
            ("▱", "System information", "Check your Mac's hardware and status.", "System information"),
        ]

        quick_actions = QWidget()
        quick_actions.setObjectName("quickActions")
        quick_actions.setMaximumWidth(1140)
        quick_actions.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        grid = QHBoxLayout(quick_actions)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(10)

        for index, (symbol, title, description, message) in enumerate(prompts):
            button = QPushButton()
            button.setObjectName("promptCard")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(156)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )

            card_layout = QVBoxLayout(button)
            card_layout.setContentsMargins(14, 12, 14, 12)
            card_layout.setSpacing(6)

            top_row = QHBoxLayout()
            top_row.setContentsMargins(0, 0, 0, 0)

            icon = QLabel(symbol)
            icon.setObjectName("promptIcon")
            icon.setProperty("tone", str(index))
            icon.setFixedSize(48, 48)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

            arrow = QLabel("›")
            arrow.setObjectName("promptArrow")
            arrow.setFixedSize(38, 38)
            arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)

            top_row.addWidget(icon)
            top_row.addStretch()
            top_row.addWidget(arrow)

            name = QLabel(title)
            name.setObjectName("promptTitle")
            name.setWordWrap(True)

            detail = QLabel(description)
            detail.setObjectName("promptDescription")
            detail.setWordWrap(True)

            card_layout.addLayout(top_row)
            card_layout.addWidget(name)
            card_layout.addWidget(detail)
            card_layout.addStretch(1)

            button.clicked.connect(
                lambda checked=False, value=message:
                self.select_prompt(value)
            )

            grid.addWidget(button, 1)

        quick_actions_row = QHBoxLayout()
        quick_actions_row.setContentsMargins(0, 0, 0, 0)
        quick_actions_row.addStretch()
        quick_actions_row.addWidget(quick_actions, 1)
        quick_actions_row.addStretch()

        layout.addLayout(quick_actions_row)
        layout.addStretch(2)

        return page

    def create_composer(self):
        self.composer = QFrame()
        self.composer.setObjectName("composer")

        outer = QVBoxLayout(self.composer)
        outer.setContentsMargins(12, 8, 12, 8)
        outer.setSpacing(4)

        row = QHBoxLayout()
        row.setSpacing(8)

        self.input = QLineEdit()
        self.input.setObjectName("messageInput")
        self.input.setPlaceholderText("Message IRIS...")
        self.input.setClearButtonEnabled(True)
        self.input.returnPressed.connect(self.send_message)

        self.voice_button = QPushButton()
        self.voice_button.setObjectName("iconButton")
        self.voice_button.setFixedSize(42, 42)
        self.voice_button.setIcon(voice_icon("microphone"))
        self.voice_button.setIconSize(QSize(20, 20))
        self.voice_button.setToolTip("Talk to IRIS")
        self.voice_button.setAccessibleName("Voice input")
        self.voice_button.clicked.connect(self.start_voice_input)

        self.send_button = QPushButton("↑")
        self.send_button.setObjectName("sendButton")
        self.send_button.setFixedSize(42, 42)
        self.send_button.setToolTip("Send message")
        self.send_button.clicked.connect(self.send_message)

        row.addWidget(self.input, 1)
        row.addWidget(self.voice_button)
        row.addWidget(self.send_button)

        footer = QHBoxLayout()

        self.activity_label = QLabel("Ready when you are")
        self.activity_label.setObjectName("composerHint")

        local_label = QLabel("Local model · Ollama")
        local_label.setObjectName("composerHint")

        footer.addWidget(self.activity_label)
        footer.addStretch()
        footer.addWidget(local_label)

        outer.addLayout(row)
        outer.addLayout(footer)

    def conversation_summaries(self):
        return sorted(
            self.conversations,
            key=lambda conversation: conversation.get("updated_at", ""),
            reverse=True,
        )

    def persist_conversations(self):
        try:
            self.conversation_store.save_document(
                {"version": 1, "conversations": self.conversations}
            )
        except OSError as error:
            self.conversation_error.emit(
                f"Could not save conversation history: {error}"
            )
            return False

        self.conversations_changed.emit()
        return True

    def new_conversation(self):
        timestamp = datetime.now().isoformat(timespec="seconds")
        return {
            "id": uuid4().hex,
            "title": "New conversation",
            "created_at": timestamp,
            "updated_at": timestamp,
            "messages": [],
        }

    def active_conversation(self, create=False):
        for conversation in self.conversations:
            if conversation.get("id") == self.active_conversation_id:
                return conversation

        if not create:
            return None

        conversation = self.new_conversation()
        self.conversations.append(conversation)
        self.active_conversation_id = conversation["id"]
        return conversation

    def has_conversation(self, conversation_id):
        return any(
            conversation.get("id") == conversation_id
            for conversation in self.conversations
        )

    def rename_conversation(self, conversation_id, title):
        title = " ".join(title.split())
        if not title:
            return False

        conversation = next(
            (
                item for item in self.conversations
                if item.get("id") == conversation_id
            ),
            None,
        )
        if conversation is None:
            return False

        previous_title = conversation.get("title", "New conversation")
        conversation["title"] = title
        if not self.persist_conversations():
            conversation["title"] = previous_title
            return False

        return True

    def duplicate_conversation(self, conversation_id):
        conversation = next(
            (
                item for item in self.conversations
                if item.get("id") == conversation_id
            ),
            None,
        )
        if conversation is None:
            return None

        duplicate = self.new_conversation()
        duplicate["title"] = f"{conversation.get('title', 'Conversation')} copy"
        duplicate["messages"] = [
            dict(message) for message in conversation.get("messages", [])
        ]
        self.conversations.append(duplicate)
        if not self.persist_conversations():
            self.conversations.remove(duplicate)
            return None

        return duplicate["id"]

    def delete_conversation(self, conversation_id):
        if not self.has_conversation(conversation_id):
            return False

        previous_conversations = self.conversations
        self.conversations = [
            conversation for conversation in self.conversations
            if conversation.get("id") != conversation_id
        ]
        if not self.persist_conversations():
            self.conversations = previous_conversations
            return False

        if self.active_conversation_id == conversation_id:
            self.last_user_message = ""
            self.active_conversation_id = None
            self.clear_rendered_messages()
            self.input.clear()
            self.chat_stack.setCurrentWidget(self.welcome_page)

        if self.active_request_conversation_id == conversation_id:
            self.discard_pending_response = True
            self.active_request = None
            self.active_request_conversation_id = None
            self.remove_thinking()
            self.set_busy(False, "Conversation deleted")

        self.conversations_changed.emit()
        return True

    def save_message(self, role, content, conversation_id=None):
        if conversation_id and conversation_id != self.active_conversation_id:
            conversation = next(
                (
                    item for item in self.conversations
                    if item.get("id") == conversation_id
                ),
                None,
            )
        else:
            conversation = self.active_conversation(create=True)

        if conversation is None:
            return
        conversation["messages"].append(
            {
                "role": role,
                "content": str(content),
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        )
        conversation["updated_at"] = datetime.now().isoformat(
            timespec="seconds"
        )

        if role == "user" and conversation["title"] == "New conversation":
            title = " ".join(str(content).split())
            conversation["title"] = (
                f"{title[:47].rstrip()}…" if len(title) > 48 else title
            ) or "New conversation"

        self.persist_conversations()

    def clear_rendered_messages(self):
        self.remove_thinking()

        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.message_bubbles.clear()
        self.regenerate_buttons.clear()

    def load_conversation(self, conversation_id):
        if self.closing or self.is_busy:
            return False

        conversation = next(
            (
                item for item in self.conversations
                if item.get("id") == conversation_id
            ),
            None,
        )
        if conversation is None:
            return False

        self.clear_rendered_messages()
        self.active_conversation_id = conversation_id
        self.last_user_message = ""

        for message in conversation.get("messages", []):
            role = message.get("role")
            content = message.get("content", "")
            if role == "user":
                self.last_user_message = content
                self.add_message(
                    "You",
                    content,
                    timestamp=message.get("created_at"),
                )
            elif role == "assistant":
                self.add_message(
                    "IRIS",
                    content,
                    self.last_user_message,
                    message.get("created_at"),
                )

        self.chat_stack.setCurrentWidget(self.scroll_area)
        self.set_busy(False, "Ready when you are")
        self.conversations_changed.emit()
        return True

    def start_new_chat(self):
        if self.closing or self.is_busy:
            return

        self.last_user_message = ""
        self.active_request = None
        self.active_conversation_id = None
        self.active_request_conversation_id = None
        self.clear_rendered_messages()
        self.input.clear()
        self.chat_stack.setCurrentWidget(self.welcome_page)
        self.set_busy(False, "Ready for a new conversation")
        self.conversations_changed.emit()

    def create_workers(self):
        self.thread = QThread(self)
        self.worker = IRISWorker()
        self.worker.moveToThread(self.thread)

        self.process_message.connect(self.worker.process)
        self.execute_approved.connect(self.worker.execute_message)

        self.worker.finished.connect(self.handle_response)
        self.worker.error.connect(self.handle_error)
        self.worker.permission_required.connect(
            self.handle_permission_request
        )

        self.thread.start()

        self.voice_thread = QThread(self)
        self.voice_worker = VoiceWorker()
        self.voice_worker.moveToThread(self.voice_thread)

        self.start_voice.connect(self.voice_worker.listen)
        self.stop_voice.connect(self.voice_worker.stop)

        self.voice_worker.finished.connect(self.handle_voice_result)
        self.voice_worker.error.connect(self.handle_voice_error)

        self.voice_thread.start()

        self.speech_thread = QThread(self)
        self.speech_worker = SpeechWorker()
        self.speech_worker.moveToThread(self.speech_thread)

        self.speak_response.connect(self.speech_worker.speak)
        self.stop_speech.connect(self.speech_worker.stop)

        self.speech_worker.error.connect(self.handle_speech_error)

        self.speech_thread.start()

   
    def select_prompt(self, message):
        self.input.setText(message)
        self.input.setFocus()
        self.input.setCursorPosition(len(message))

        if message.strip() in (
            "Find file",
            "Search web for",
            "Open Application",
        ):
            return

        self.send_message()


    def add_message(
        self,
        sender,
        message,
        request_message=None,
        timestamp=None,
    ):
        row = QWidget()
        row.setObjectName("messageRow")

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(10)

        bubble = QFrame()
        bubble.setObjectName(
            "userBubble" if sender == "You" else "irisBubble"
        )
        bubble.setMaximumWidth(980 if sender != "You" else 680)
        bubble.setMinimumWidth(0)
        bubble.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Preferred,
        )
        bubble.setProperty("assistantMessage", sender != "You")
        self.message_bubbles.append(bubble)

        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(14, 9, 14, 9)
        bubble_layout.setSpacing(4)

        sender_label = QLabel(sender)
        sender_label.setObjectName("messageSender")

        timestamp_label = QLabel(self.format_message_time(timestamp))
        timestamp_label.setObjectName("messageTime")
        timestamp_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        message_header = QHBoxLayout()
        message_header.setContentsMargins(0, 0, 0, 0)
        message_header.addWidget(sender_label)
        message_header.addStretch()
        message_header.addWidget(timestamp_label)

        display_message = str(message).strip()
        bubble.setProperty(
            "wideUserMessage",
            sender == "You" and len(display_message) > 40,
        )
        bubble.setProperty(
            "wideAssistantMessage",
            sender != "You" and len(display_message) > 180,
        )

        if (
            sender != "You"
            and len(display_message) > 320
            and "\n" not in display_message
        ):
            sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", display_message)
            if len(sentences) >= 3:
                paragraphs = []
                for index in range(0, len(sentences), 2):
                    paragraph = " ".join(sentences[index:index + 2]).strip()
                    if paragraph:
                        paragraphs.append(paragraph)
                display_message = "\n\n".join(paragraphs)

        message_text, sources_text = self.split_sources_section(
            display_message
        )
        message_label = self.create_message_label(
            message_text or display_message,
            "messageText",
        )

        bubble_layout.addLayout(message_header)
        bubble_layout.addWidget(message_label)

        if sources_text:
            sources = QFrame()
            sources.setObjectName("sourcesSection")

            sources_layout = QVBoxLayout(sources)
            sources_layout.setContentsMargins(10, 9, 10, 9)
            sources_layout.setSpacing(5)

            sources_heading = QLabel("SOURCES")
            sources_heading.setObjectName("sourcesHeading")

            sources_label = self.create_message_label(
                sources_text,
                "sourcesText",
            )

            sources_layout.addWidget(sources_heading)
            sources_layout.addWidget(sources_label)
            bubble_layout.addWidget(sources)

        if sender != "You":
            actions = QHBoxLayout()
            actions.setContentsMargins(0, 4, 0, 0)
            actions.setSpacing(8)

            copy_button = QPushButton("⧉")
            copy_button.setObjectName("messageAction")
            copy_button.setFixedSize(28, 28)
            copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
            copy_button.setToolTip("Copy this response")
            copy_button.clicked.connect(
                lambda checked=False, value=str(message), button=copy_button:
                self.copy_message(value, button)
            )
            actions.addWidget(copy_button)

            # Show Open only when this response contains an existing file path.
            file_paths = self.extract_existing_file_paths(str(message))

            if file_paths:
                open_button = QPushButton("↗")
                open_button.setObjectName("messageAction")
                open_button.setFixedSize(28, 28)
                open_button.setCursor(Qt.CursorShape.PointingHandCursor)
                open_button.setToolTip("Open a file from this response")
                open_button.clicked.connect(
                    lambda checked=False, paths=file_paths:
                    self.choose_file_to_open(paths)
                )
                actions.addWidget(open_button)


            regenerate_button = QPushButton("↻")
            regenerate_button.setObjectName("messageAction")
            regenerate_button.setFixedSize(28, 28)
            regenerate_button.setCursor(Qt.CursorShape.PointingHandCursor)
            regenerate_button.setToolTip("Generate another response")
            regenerate_message = request_message
            regenerate_button.setProperty(
                "hasRegenerateRequest",
                bool(regenerate_message),
            )
            regenerate_button.setEnabled(
                bool(regenerate_message) and not self.is_busy
            )
            regenerate_button.clicked.connect(
                lambda checked=False, value=regenerate_message:
                self.regenerate_response(value)
            )
            self.regenerate_buttons.append(regenerate_button)
            actions.addWidget(regenerate_button)
            actions.addStretch()

            bubble_layout.addLayout(actions)

        if sender == "You":
            row_layout.addStretch()
            row_layout.addWidget(
                bubble,
                0,
                Qt.AlignmentFlag.AlignRight,
            )
        else:
            avatar = QLabel("◎")
            avatar.setObjectName("messageAvatar")
            avatar.setFixedSize(44, 44)
            avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

            row_layout.addWidget(
                avatar,
                0,
                Qt.AlignmentFlag.AlignTop,
            )
            row_layout.addWidget(bubble)
            row_layout.addStretch()

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            row,
        )

        self.update_bubble_widths()
        self.scroll_to_bottom()

    
    def extract_existing_file_paths(self, text):
        import re

        paths = []
        pattern = re.compile(
            r"(?<!\S)/(?:Users|Volumes|tmp)/[^\n\r<>\"']+"
        )

        for match in pattern.finditer(text):
            path = match.group(0).rstrip(".,;:)")
            if os.path.isfile(path) and path not in paths:
                paths.append(path)

        return paths[:10]

    def choose_file_to_open(self, paths):
        if len(paths) == 1:
            path = paths[0]
        else:
            path, accepted = QInputDialog.getItem(
                self,
                "Open file",
                "Choose a file:",
                paths,
                0,
                False,
            )
            if not accepted or not path:
                return

        try:
            subprocess.Popen(["open", path])
        except OSError as error:
            QMessageBox.warning(
                self,
                "Could not open file",
                str(error),
            )

    def format_message_time(self, timestamp):
        if timestamp:
            try:
                return datetime.fromisoformat(timestamp).strftime(
                    "%I:%M %p"
                ).lstrip("0")
            except (TypeError, ValueError):
                pass

        return datetime.now().strftime("%I:%M %p").lstrip("0")

    def create_message_label(self, text, object_name):
        message_label = QLabel()
        message_label.setObjectName(object_name)
        if object_name == "messageText":
            document = QTextDocument()
            document_font = QFont("Helvetica Neue")
            document_font.setPixelSize(16)
            document.setDefaultFont(document_font)
            document.setDefaultStyleSheet("""
                p { margin: 0 0 13px 0; line-height: 150%; }
                h1, h2, h3, h4, h5, h6 {
                    margin: 4px 0 8px 0;
                    font-weight: 700;
                }
                ol, ul { margin: 7px 0 13px 0; padding-left: 28px; }
                li { margin: 0 0 8px 0; line-height: 150%; }
                pre { margin: 8px 0; }
            """)
            document.setMarkdown(text)
            cursor = QTextCursor(document)
            cursor.select(QTextCursor.SelectionType.Document)
            block_format = QTextBlockFormat()
            block_format.setLineHeight(140, 1)
            block_format.setBottomMargin(8)
            cursor.mergeBlockFormat(block_format)
            message_label.setText(document.toHtml())
            message_label.setTextFormat(Qt.TextFormat.RichText)
        else:
            message_label.setText(text)
            message_label.setTextFormat(Qt.TextFormat.MarkdownText)
        message_label.setOpenExternalLinks(True)
        message_label.setWordWrap(True)
        message_label.setMinimumWidth(0)
        message_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        return message_label

    def split_sources_section(self, message):
        section_match = re.search(
            r"(?im)^(?:#{1,6}\s*)?sources?\s*:?\s*\n",
            message,
        )

        if section_match:
            return (
                message[:section_match.start()].rstrip(),
                message[section_match.end():].strip(),
            )

        inline_match = re.search(
            r"\s+sources?\s*:\s+(?=(?:\[|https?://))",
            message,
            flags=re.IGNORECASE,
        )

        if inline_match:
            return (
                message[:inline_match.start()].rstrip(),
                message[inline_match.end():].strip(),
            )

        return message, ""

    def add_thinking(self, text="IRIS is thinking..."):
        self.remove_thinking()

        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(40, 0, 0, 0)
        layout.setSpacing(8)

        dot = QLabel("●")
        dot.setObjectName("thinkingDot")

        label = QLabel(text)
        label.setObjectName("thinking")

        layout.addWidget(dot)
        layout.addWidget(label)
        layout.addStretch()

        self.thinking_widget = row

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            row,
        )

        self.activity_label.setText(text)
        self.scroll_to_bottom()

    def remove_thinking(self):
        if self.thinking_widget is None:
            return

        self.chat_layout.removeWidget(self.thinking_widget)
        self.thinking_widget.deleteLater()
        self.thinking_widget = None

    def scroll_to_bottom(self):
        QTimer.singleShot(0, self.scroll_to_latest_message)

    def scroll_to_latest_message(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_bubble_widths(self):
        available_width = self.scroll_area.viewport().width()

        if available_width <= 0:
            return

        maximum_width = min(860, max(340, int(available_width * 0.78)))

        for bubble in self.message_bubbles:
            bubble.setMaximumWidth(maximum_width)
            if bubble.property("wideAssistantMessage"):
                bubble.setMinimumWidth(
                    min(maximum_width, max(480, int(available_width * 0.72)))
                )
            elif bubble.property("wideUserMessage"):
                bubble.setMinimumWidth(
                    min(420, int(available_width * 0.42))
                )
            else:
                bubble.setMinimumWidth(0)

    def set_busy(self, busy, status=None):
        self.is_busy = busy
        self.send_button.setEnabled(not busy)
        self.voice_button.setEnabled(not busy)
        self.input.setEnabled(not busy)

        for button in self.regenerate_buttons:
            button.setEnabled(
                not busy and bool(button.property("hasRegenerateRequest"))
            )

        if status:
            self.activity_label.setText(status)

        if not busy:
            self.input.setFocus()

    def send_message(self):
        if self.closing:
            return

        message = self.input.text().strip()

        if not message:
            return

        self.chat_stack.setCurrentWidget(self.scroll_area)

        self.last_user_message = message
        self.active_request = message
        self.save_message("user", message)
        self.active_request_conversation_id = self.active_conversation_id
        self.add_message("You", message)
        self.input.clear()

        self.set_busy(True, "Working on your request...")
        self.add_thinking()

        self.process_message.emit(message)

    def start_voice_input(self):
        if self.closing:
            return

        self.chat_stack.setCurrentWidget(self.scroll_area)

        self.set_busy(True, "Listening...")
        self.add_thinking("IRIS is listening...")

        self.start_voice.emit()

    def handle_voice_result(self, text):
        if self.closing:
            return

        self.remove_thinking()

        if not text:
            message = "I didn't hear anything. Try again."
            self.add_message("IRIS", message)
            self.set_busy(False, "Ready when you are")
            return

        self.last_user_message = text
        self.active_request = text
        self.save_message("user", text)
        self.active_request_conversation_id = self.active_conversation_id
        self.add_message("You", text)
        self.add_thinking()
        self.activity_label.setText("Processing your voice message...")
        self.process_message.emit(text)

    def copy_message(self, message, button=None):
        QApplication.clipboard().setText(message)

        if button is None:
            return

        button.setText("Copied")
        QTimer.singleShot(
            1200,
            lambda: self.restore_copy_button(button),
        )

    def restore_copy_button(self, button):
        if not self.closing:
            button.setText("Copy")

    def regenerate_response(self, message=None):
        if self.closing or self.is_busy:
            return

        request_message = message or self.last_user_message

        if not request_message:
            return

        self.chat_stack.setCurrentWidget(self.scroll_area)
        self.set_busy(True, "Regenerating response...")
        self.add_thinking("IRIS is generating another response...")
        self.active_request = request_message
        self.active_request_conversation_id = self.active_conversation_id
        self.process_message.emit(request_message)

    def handle_voice_error(self, error):
        if self.closing:
            return

        self.remove_thinking()
        message = f"Voice input error: {error}"
        self.add_message("IRIS", message)
        self.set_busy(False, "Ready when you are")

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled

        if self.audio_enabled:
            self.header_audio_button.setIcon(voice_icon("speaker"))
            self.audio_status.setText("Voice on")
            self.header_audio_button.setToolTip(
                "Turn voice responses off"
            )
        else:
            self.header_audio_button.setIcon(voice_icon("speaker", muted=True))
            self.audio_status.setText("Voice off")
            self.header_audio_button.setToolTip(
                "Turn voice responses on"
            )
            self.stop_speech.emit()

    def handle_permission_request(self, action, message):
        if self.closing:
            return

        box = QMessageBox(self)
        box.setWindowTitle("IRIS Permission Request")
        box.setIcon(QMessageBox.Icon.Warning)
        box.setText(f"IRIS wants to perform '{action}'.")
        box.setInformativeText(
            f"Request:\n{message}\n\nAllow this action?"
        )

        allow = box.addButton(
            "Allow",
            QMessageBox.ButtonRole.AcceptRole,
        )
        box.addButton(
            "Deny",
            QMessageBox.ButtonRole.RejectRole,
        )

        box.exec()

        if box.clickedButton() == allow:
            response = "Permission granted."
            self.add_message("IRIS", response)
            self.save_message(
                "assistant",
                response,
                self.active_request_conversation_id,
            )
            self.execute_approved.emit(message)
        else:
            response = "Permission denied."
            self.add_message("IRIS", response)
            self.save_message(
                "assistant",
                response,
                self.active_request_conversation_id,
            )
            self.handle_response("I did not perform that action.")

    def handle_response(self, response):
        if self.closing:
            return

        if self.discard_pending_response:
            self.discard_pending_response = False
            self.remove_thinking()
            self.set_busy(False, "Conversation deleted")
            return

        self.remove_thinking()
        request_message = self.active_request
        request_conversation_id = self.active_request_conversation_id
        self.active_request = None
        self.active_request_conversation_id = None
        self.add_message("IRIS", response, request_message)
        self.save_message("assistant", response, request_conversation_id)

        if self.audio_enabled:
            self.speak_response.emit(response)

        self.set_busy(False, "Ready when you are")

    def handle_error(self, error):
        if self.closing:
            return

        if self.discard_pending_response:
            self.discard_pending_response = False
            self.remove_thinking()
            self.set_busy(False, "Conversation deleted")
            return

        self.remove_thinking()
        self.active_request = None
        request_conversation_id = self.active_request_conversation_id
        self.active_request_conversation_id = None
        message = f"Something went wrong: {error}"
        self.add_message("IRIS", message)
        self.save_message("assistant", message, request_conversation_id)
        self.set_busy(False, "An error occurred")

    def handle_speech_error(self, error):
        if self.closing:
            return

        message = f"Voice output error: {error}"
        self.add_message("IRIS", message)
        self.save_message(
            "assistant",
            message,
            self.active_conversation_id,
        )

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget#chatWidget {
                background: #17191C;
                color: #F1F3F5;
                font-family: "Helvetica Neue", Arial;
            }

            QFrame#chatHeader {
                background: #151E29;
                border: 1px solid #263341;
                border-radius: 14px;
            }

            QLabel#headerAvatar, QLabel#messageAvatar {
                background: #123B70;
                color: #D8EDFF;
                border: 1px solid #2166B6;
                border-radius: 12px;
                font-size: 25px;
                font-weight: bold;
            }

            QLabel#headerTitle {
                color: #F1F5F9;
                font-size: 18px;
                font-weight: 700;
            }

            QLabel#headerSubtitle {
                color: #A4ABB5;
                font-size: 14px;
            }

            QLabel#audioStatus {
                color: #A4ABB5;
                font-size: 14px;
            }

            QStackedWidget#chatStack,
            QWidget#welcomePage,
            QScrollArea#chatScroll,
            QWidget#chatContainer {
                background: #17191C;
                border: none;
            }

            QLabel#welcomeTitle {
                color: #F6F8FC;
                font-size: 34px;
                font-weight: 800;
            }

            QLabel#welcomeSubtitle {
                color: #AAB6C8;
                font-size: 17px;
            }

            QPushButton#promptCard {
                background: #15202D;
                color: #E9ECF0;
                border: 1px solid #2A394A;
                border-radius: 16px;
                text-align: left;
            }

            QPushButton#promptCard:hover {
                background: #1A2939;
                border: 1px solid #4773A4;
            }

            QPushButton#promptCard:pressed {
                background: #172D45;
                border: 1px solid #2F8CFF;
            }

            QLabel#promptIcon {
                background: #174F91;
                color: #AEE9FF;
                border: none;
                border-radius: 14px;
                font-size: 23px;
                font-weight: bold;
            }

            QLabel#promptIcon[tone="1"] {
                background: #493870;
                color: #D9B8FF;
            }

            QLabel#promptIcon[tone="2"] {
                background: #136452;
                color: #7CFFCE;
            }

            QLabel#promptIcon[tone="3"] {
                background: #75431F;
                color: #FFD09B;
            }

            QLabel#promptArrow {
                background: #1D3550;
                color: #75BBFF;
                border: none;
                border-radius: 19px;
                font-size: 28px;
                font-weight: 400;
            }

            QLabel#promptTitle {
                color: #E9ECF0;
                font-size: 15px;
                font-weight: 700;
            }

            QLabel#promptDescription {
                color: #B5C0CF;
                font-size: 12px;
                line-height: 1.3;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 7px;
                margin: 3px;
            }

            QScrollBar::handle:vertical {
                background: #303747;
                border-radius: 3px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #475569;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }

            QFrame#userBubble {
                background: #2E5A87;
                border: none;
                border-radius: 10px;
            }

            QFrame#irisBubble {
                background: #20242A;
                border: 1px solid #303640;
                border-radius: 10px;
            }

            QFrame#sourcesSection {
                background: #1B1E23;
                border: 1px solid #303640;
                border-radius: 7px;
            }

            QLabel#messageSender {
                color: #A4ABB5;
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#messageTime {
                color: #8E9AAC;
                font-size: 10px;
            }

            QFrame#userBubble QLabel#messageSender {
                color: #E1EBF5;
            }

            QFrame#userBubble QLabel#messageTime {
                color: #C7DCF2;
            }

            QLabel#messageText {
                color: #F1F5F9;
                font-size: 14px;
                padding:   0;
            }

            QLabel#sourcesHeading {
                color: #78818D;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#sourcesText {
                color: #C8CDD3;
                font-size: 12px;
            }

            QPushButton#messageAction {
                background: transparent;
                color: #78818D;
                border: none;
                border-radius: 5px;
                padding: 4px 7px;
                font-size: 17px;
            }

            QPushButton#messageAction:hover {
                background: #2A2F36;
                color: #F1F3F5;
            }

            QPushButton#messageAction:disabled {
                color: #475569;
            }

            QLabel#thinking {
                color: #A4ABB5;
                font-size: 12px;
            }

            QLabel#thinkingDot {
                color: #3988F5;
                font-size: 11px;
            }

            QFrame#composer {
                background: #151E29;
                border: 1px solid #263341;
                border-radius: 14px;
            }

            QLineEdit#messageInput {
                background: #172230;
                color: #F1F3F5;
                border: 1px solid #2F8CFF;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 15px;
                selection-background-color: #315A99;
            }

            QLineEdit#messageInput:focus {
                border: 1px solid #59A7FF;
            }

            QPushButton#iconButton {
                background: #1C2B3E;
                color: #D7DCE2;
                border: 1px solid #314965;
                border-radius: 12px;
                font-size: 21px;
            }

            QPushButton#iconButton:hover {
                background: #263B54;
                border: 1px solid #5AA8FF;
            }

            QPushButton#sendButton {
                background: #3988F5;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 30px;
                font-weight: bold;
            }

            QPushButton#sendButton:hover {
                background: #4A96FF;
            }

            QPushButton#sendButton:disabled,
            QPushButton#iconButton:disabled {
                background: #24282E;
                color: #78818D;
            }

            QLabel#composerHint {
                color: #7186A5;
                font-size: 10px;
            }


            QMessageBox {
                background: #161922;
                color: #F1F5F9;
            }

            QMessageBox QLabel {
                color: #F1F5F9;
            }

            QMessageBox QPushButton {
                background: #232736;
                color: #F1F5F9;
                border: 1px solid #343B4D;
                border-radius: 7px;
                padding: 7px 16px;
                min-width: 65px;
            }

            QMessageBox QPushButton:hover {
                background: #30394D;
            }
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.update_bubble_widths)

    def shutdown_workers(self):
        if self.closing:
            return all(
                not thread.isRunning()
                for thread in (
                    self.thread,
                    self.voice_thread,
                    self.speech_thread,
                )
            )

        self.closing = True

        self.set_busy(True)
        self.stop_voice.emit()
        self.stop_speech.emit()

        for thread in (
            self.thread,
            self.voice_thread,
            self.speech_thread,
        ):
            thread.quit()

        return all(
            thread.wait(2500)
            for thread in (
                self.thread,
                self.voice_thread,
                self.speech_thread,
            )
        )

    def closeEvent(self, event):
        if self.shutdown_workers():
            event.accept()
        else:
            event.ignore()
