from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton
)

from PySide6.QtCore import Qt

from app.chat import ChatWidget


class IRISWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IRIS V3.0")
        self.resize(1450, 900)
        self.setMinimumSize(1150, 720)

        central = QWidget()
        central.setObjectName("central")

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            18,
            16,
            18,
            18
        )

        main_layout.setSpacing(12)

        header = self.create_header()

        content = QHBoxLayout()
        content.setSpacing(12)

        chat_panel = self.create_chat_panel()
        right_panel = self.create_right_panel()

        content.addWidget(
            chat_panel,
            1
        )

        content.addWidget(
            right_panel
        )

        main_layout.addWidget(
            header
        )

        main_layout.addLayout(
            content,
            1
        )

        central.setLayout(
            main_layout
        )

        self.setCentralWidget(
            central
        )

        self.setStyleSheet("""
            QMainWindow {
                background: #0F1117;
            }

            QWidget#central {
                background: #0F1117;
                color: #F1F5F9;
                font-family: Arial;
            }


            /* =========================
               HEADER
               ========================= */

            QFrame#header {
                background: #12151C;
                border: 1px solid #252B38;
                border-radius: 16px;
            }

            QFrame#logo {
                background: qlineargradient(
                    x1: 0,
                    y1: 0,
                    x2: 1,
                    y2: 1,
                    stop: 0 #3B82F6,
                    stop: 1 #6366F1
                );

                border: none;
                border-radius: 29px;
            }

            QLabel#logoText {
                color: #FFFFFF;
                font-size: 24px;
                font-weight: bold;
            }

            QLabel#brand {
                color: #F8FAFC;
                font-size: 26px;
                font-weight: bold;
            }

            QLabel#brandSub {
                color: #94A3B8;
                font-size: 12px;
            }

            QLabel#version {
                background: #1E293B;
                color: #94A3B8;

                border: 1px solid #2A3042;
                border-radius: 9px;

                padding: 7px 12px;

                font-size: 11px;
                font-weight: bold;
            }

            QLabel#online {
                color: #4ADE80;
                font-size: 12px;
                font-weight: 600;
            }


            /* =========================
               CHAT PANEL
               ========================= */

            QFrame#chatPanel {
                background: #0F1117;
                border: 1px solid #242A37;
                border-radius: 16px;
            }


            /* =========================
               MESSAGE BUBBLES
               ========================= */

            QFrame#userBubble {
                background: #2563EB;
                border: none;
                border-radius: 16px;
            }

            QFrame#irisBubble {
                background: #1E2330;
                border: 1px solid #2A3042;
                border-radius: 16px;
            }

            QLabel#messageSender {
                color: #94A3B8;
                font-size: 10px;
                font-weight: 600;
            }

            QFrame#userBubble QLabel#messageSender {
                color: #DBEAFE;
            }

            QLabel#messageText {
                color: #F1F5F9;
                font-size: 14px;
            }

            QLabel#thinking {
                color: #64748B;
                font-size: 11px;
                font-style: italic;
            }


            /* =========================
               AVATARS
               ========================= */

            QFrame#avatar {
                background: #232736;
                border: 1px solid #343B4D;
                border-radius: 16px;
            }

            QLabel#avatarText {
                color: #60A5FA;
                font-size: 14px;
                font-weight: bold;
            }

            QFrame#userAvatar {
                background: #312E81;
                border: 1px solid #4338CA;
                border-radius: 16px;
            }

            QLabel#userAvatarText {
                color: #E0E7FF;
                font-size: 11px;
                font-weight: bold;
            }


            /* =========================
               COMPOSER
               ========================= */

            QFrame#composer {
                background: #181B24;

                border: 1px solid #2A3042;
                border-radius: 14px;
            }

            QFrame#composer:focus-within {
                border: 1px solid #3B82F6;
            }

            QLineEdit {
                background: transparent;

                color: #F1F5F9;

                border: none;

                padding: 12px 7px;

                font-size: 14px;
            }

            QLineEdit:focus {
                border: none;
            }

            QLineEdit::placeholder {
                color: #64748B;
            }

            QPushButton#composerSecondary {
                background: #1E2330;

                color: #94A3B8;

                border: 1px solid #2A3042;
                border-radius: 10px;

                font-size: 18px;
            }

            QPushButton#composerSecondary:hover {
                background: #282F40;
                color: #E2E8F0;
                border: 1px solid #3B82F6;
            }

            QPushButton#sendButton {
                background: #3B82F6;

                color: #FFFFFF;

                border: none;
                border-radius: 10px;

                font-size: 19px;
                font-weight: bold;
            }

            QPushButton#sendButton:hover {
                background: #2563EB;
            }

            QPushButton#sendButton:pressed {
                background: #1D4ED8;
            }


            /* =========================
               RIGHT SIDEBAR
               ========================= */

            QFrame#rightPanel {
                background: #161922;

                border: 1px solid #242A37;
                border-radius: 16px;
            }

            QLabel#capabilityHeader {
                color: #F8FAFC;
                font-size: 23px;
                font-weight: 600;
            }

            QLabel#capabilitySubtitle {
                color: #64748B;
                font-size: 11px;
            }


            /* =========================
               CAPABILITY CARDS
               ========================= */

            QFrame#capability {
                background: #1F2430;

                border: 1px solid #2A3142;
                border-radius: 12px;
            }

            QFrame#capability:hover {
                background: #282F40;
                border: 1px solid #3B82F6;
            }

            QLabel#capabilityIcon {
                background: #262D3D;

                color: #60A5FA;

                border: none;
                border-radius: 10px;

                font-size: 20px;
                font-weight: bold;
            }

            QLabel#capabilityTitle {
                color: #F1F5F9;

                font-size: 12px;
                font-weight: 600;
            }

            QLabel#capabilitySub {
                color: #64748B;

                font-size: 9px;
            }

            QLabel#capabilityArrow {
                color: #64748B;
                font-size: 21px;
            }

            QPushButton#sidebarButton {
                background: #1E2330;

                color: #94A3B8;

                border: 1px solid #2A3042;
                border-radius: 10px;

                font-size: 17px;
            }

            QPushButton#sidebarButton:hover {
                background: #282F40;
                color: #F1F5F9;
                border: 1px solid #3B82F6;
            }
        """)

    def create_header(self):
        header = QFrame()
        header.setObjectName("header")

        layout = QHBoxLayout()

        layout.setContentsMargins(
            18,
            11,
            18,
            11
        )

        logo = QFrame()
        logo.setObjectName("logo")

        logo.setFixedSize(
            58,
            58
        )

        logo_layout = QVBoxLayout()

        logo_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        logo_text = QLabel("◉")

        logo_text.setObjectName(
            "logoText"
        )

        logo_text.setAlignment(
            Qt.AlignCenter
        )

        logo_layout.addWidget(
            logo_text
        )

        logo.setLayout(
            logo_layout
        )

        identity = QVBoxLayout()
        identity.setSpacing(1)

        title = QLabel("IRIS")
        title.setObjectName("brand")

        subtitle = QLabel(
            "Your Personal AI Assistant"
        )

        subtitle.setObjectName(
            "brandSub"
        )

        identity.addWidget(title)
        identity.addWidget(subtitle)

        layout.addWidget(logo)
        layout.addSpacing(10)
        layout.addLayout(identity)

        layout.addStretch()

        version = QLabel("V3.0")
        version.setObjectName("version")

        online = QLabel("● Online")
        online.setObjectName("online")

        layout.addWidget(version)
        layout.addSpacing(12)
        layout.addWidget(online)

        header.setLayout(layout)

        return header

    def create_chat_panel(self):
        panel = QFrame()

        panel.setObjectName(
            "chatPanel"
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            8,
            8,
            8,
            8
        )

        self.chat = ChatWidget()

        layout.addWidget(
            self.chat
        )

        panel.setLayout(
            layout
        )

        return panel

    def create_right_panel(self):
        panel = QFrame()

        panel.setObjectName(
            "rightPanel"
        )

        panel.setFixedWidth(
            310
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            16,
            18,
            16,
            18
        )

        layout.setSpacing(
            9
        )

        top = QHBoxLayout()
        top.setSpacing(6)
        top.addStretch()

        for icon in [
            "⌕",
            "☼",
            "↗"
        ]:
            button = QPushButton(icon)

            button.setObjectName(
                "sidebarButton"
            )

            button.setFixedSize(
                40,
                40
            )

            top.addWidget(button)

        layout.addLayout(top)

        layout.addSpacing(7)

        title = QLabel(
            "Capabilities"
        )

        title.setObjectName(
            "capabilityHeader"
        )

        subtitle = QLabel(
            "Everything IRIS can do"
        )

        subtitle.setObjectName(
            "capabilitySubtitle"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        capabilities = [
            (
                "✦",
                "Answer Questions",
                "AI answers & reasoning"
            ),
            (
                "□",
                "Work with Files",
                "Read, create & edit"
            ),
            (
                "⌘",
                "Control Applications",
                "Control your Mac"
            ),
            (
                "⌕",
                "Web Search",
                "Search & browse"
            ),
            (
                "◇",
                "Remember Context",
                "Long-term memory"
            ),
            (
                "🎙",
                "Voice Interaction",
                "Talk with IRIS"
            )
        ]

        for icon, name, description in capabilities:

            card = QFrame()

            card.setObjectName(
                "capability"
            )

            card.setFixedHeight(
                68
            )

            card_layout = QHBoxLayout()

            card_layout.setContentsMargins(
                10,
                9,
                10,
                9
            )

            card_layout.setSpacing(
                10
            )

            icon_label = QLabel(icon)

            icon_label.setObjectName(
                "capabilityIcon"
            )

            icon_label.setAlignment(
                Qt.AlignCenter
            )

            icon_label.setFixedSize(
                44,
                44
            )

            text_layout = QVBoxLayout()

            text_layout.setContentsMargins(
                0,
                1,
                0,
                1
            )

            text_layout.setSpacing(2)

            name_label = QLabel(name)

            name_label.setObjectName(
                "capabilityTitle"
            )

            description_label = QLabel(
                description
            )

            description_label.setObjectName(
                "capabilitySub"
            )

            text_layout.addWidget(
                name_label
            )

            text_layout.addWidget(
                description_label
            )

            arrow = QLabel("›")

            arrow.setObjectName(
                "capabilityArrow"
            )

            card_layout.addWidget(
                icon_label
            )

            card_layout.addLayout(
                text_layout
            )

            card_layout.addStretch()

            card_layout.addWidget(
                arrow
            )

            card.setLayout(
                card_layout
            )

            layout.addWidget(
                card
            )

        layout.addStretch()

        panel.setLayout(
            layout
        )

        return panel