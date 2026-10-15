
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QStackedWidget,
    QScrollArea,
    QLineEdit,
    QMenu,
    QInputDialog,
    QMessageBox,
)

from app.chat import ChatWidget


class IRISWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IRIS | Personal AI")
        self.resize(1480, 920)
        self.setMinimumSize(1100, 700)

        self.pages = {}
        self.nav_buttons = {}

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(self.create_sidebar())

        workspace = QWidget()
        workspace.setObjectName("workspace")

        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(20, 16, 20, 14)
        workspace_layout.setSpacing(10)

        workspace_layout.addWidget(self.create_header())

        self.stack = QStackedWidget()
        self.stack.setObjectName("pageStack")

        self.pages["Chat"] = self.create_chat_page()
        self.pages["Memory"] = self.create_memory_page()
        self.pages["Tools"] = self.create_tools_page()
        self.pages["Activity"] = self.create_activity_page()

        for page in self.pages.values():
            self.stack.addWidget(page)

        workspace_layout.addWidget(self.stack, 1)

        outer.addWidget(workspace, 1)

        self.right_panel = self.create_right_panel()
        outer.addWidget(self.right_panel)

        self.setStyleSheet(self.stylesheet())
        self.chat.conversations_changed.connect(
            self.refresh_conversation_history
        )
        self.chat.conversation_error.connect(self.show_conversation_error)
        self.refresh_conversation_history()
        self.navigate("Chat")

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(300)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 14, 14, 12)
        layout.setSpacing(6)

        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)

        logo = QLabel("◎")
        logo.setObjectName("logo")
        logo.setFixedSize(52, 52)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        brand_group = QVBoxLayout()
        brand_group.setSpacing(2)

        brand = QLabel("IRIS")
        brand.setObjectName("brand")

        subtitle = QLabel("PERSONAL AI")
        subtitle.setObjectName("eyebrow")

        brand_group.addWidget(brand)
        brand_group.addWidget(subtitle)

        brand_row.addWidget(logo)
        brand_row.addLayout(brand_group)
        brand_row.addStretch()

        layout.addLayout(brand_row)
        layout.addSpacing(14)

        section = QLabel("WORKSPACE")
        section.setObjectName("sectionLabel")
        layout.addWidget(section)
        layout.addSpacing(2)

        for name, symbol in [
            ("Chat", "◉"),
            ("Memory", "◇"),
            ("Tools", "⌘"),
            ("Activity", "≋"),
        ]:
            button = QPushButton(f"{symbol}     {name}")
            button.setObjectName("navButton")
            button.setMinimumHeight(42)
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False, page=name: self.navigate(page)
            )

            self.nav_buttons[name] = button
            layout.addWidget(button)

        divider = QFrame()
        divider.setObjectName("sidebarDivider")
        divider.setFrameShape(QFrame.Shape.HLine)
        layout.addSpacing(10)
        layout.addWidget(divider)
        layout.addSpacing(6)

        conversations = QHBoxLayout()
        conversations_label = QLabel("CONVERSATIONS")
        conversations_label.setObjectName("sectionLabel")
        self.conversation_search = QLineEdit()
        self.conversation_search.setObjectName("conversationSearch")
        self.conversation_search.setPlaceholderText("Search")
        self.conversation_search.setClearButtonEnabled(True)
        self.conversation_search.setMaximumWidth(92)
        self.conversation_search.textChanged.connect(
            self.refresh_conversation_history
        )
        conversations.addWidget(conversations_label)
        conversations.addStretch()
        conversations.addWidget(self.conversation_search)
        layout.addLayout(conversations)

        new_chat = QPushButton("＋  New Chat")
        new_chat.setObjectName("newChatButton")
        new_chat.setCursor(Qt.CursorShape.PointingHandCursor)
        new_chat.setMinimumHeight(42)
        new_chat.clicked.connect(lambda: self.chat.start_new_chat())
        layout.addWidget(new_chat)

        self.conversation_scroll = QScrollArea()
        self.conversation_scroll.setObjectName("conversationScroll")
        self.conversation_scroll.setWidgetResizable(True)
        self.conversation_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.conversation_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.conversation_content = QWidget()
        self.conversation_content.setObjectName("conversationContent")
        self.conversation_list = QVBoxLayout(self.conversation_content)
        self.conversation_list.setContentsMargins(0, 2, 0, 2)
        self.conversation_list.setSpacing(1)
        self.conversation_scroll.setWidget(self.conversation_content)
        layout.addWidget(self.conversation_scroll, 1)

        status = QFrame()
        status.setObjectName("statusCard")

        status_layout = QVBoxLayout(status)
        status_layout.setContentsMargins(12, 10, 12, 10)
        status_layout.setSpacing(3)

        status_heading = QLabel("LOCAL ASSISTANT")
        status_heading.setObjectName("sectionLabel")

        status_name = QLabel("IRIS V3.0")
        status_name.setObjectName("statusTitle")

        status_description = QLabel(
            "Your assistant, running on your Mac."
        )
        status_description.setObjectName("muted")
        status_description.setWordWrap(True)

        status_model = QLabel("●  Model configured · Qwen 2.5 3B")
        status_model.setObjectName("statusModel")

        status_layout.addWidget(status_heading)
        status_layout.addWidget(status_name)
        status_layout.addWidget(status_description)
        status_layout.addWidget(status_model)

        layout.addWidget(status)
        layout.addSpacing(6)

        footer = QLabel("IRIS • PERSONAL AI")
        footer.setObjectName("footer")
        layout.addWidget(footer)

        return sidebar

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def format_conversation_time(self, timestamp):
        try:
            moment = datetime.fromisoformat(timestamp)
        except (TypeError, ValueError):
            return "Earlier", ""

        today = datetime.now().date()
        if moment.date() == today:
            return "Today", moment.strftime("%I:%M %p").lstrip("0")
        if (today - moment.date()).days == 1:
            return "Yesterday", moment.strftime("%I:%M %p").lstrip("0")
        return "Earlier", moment.strftime("%b %-d")

    def refresh_conversation_history(self):
        if not hasattr(self, "conversation_list") or not hasattr(self, "chat"):
            return

        self.clear_layout(self.conversation_list)
        query = self.conversation_search.text().strip().lower()
        conversations = self.chat.conversation_summaries()

        if query:
            conversations = [
                conversation for conversation in conversations
                if query in conversation.get("title", "").lower()
                or any(
                    query in message.get("content", "").lower()
                    for message in conversation.get("messages", [])
                )
            ]

        if not conversations:
            empty = QLabel(
                "No matching conversations" if query
                else "No saved conversations yet"
            )
            empty.setObjectName("conversationEmpty")
            empty.setWordWrap(True)
            self.conversation_list.addWidget(empty)
            self.conversation_list.addStretch()
            return

        current_group = None
        for conversation in conversations:
            group, detail = self.format_conversation_time(
                conversation.get("updated_at", "")
            )
            if group != current_group:
                current_group = group
                group_label = QLabel(group.upper())
                group_label.setObjectName("conversationGroup")
                self.conversation_list.addWidget(group_label)

            row = QFrame()
            row.setObjectName("conversationRow")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(2, 0, 2, 0)
            row_layout.setSpacing(4)

            title = conversation.get("title", "New conversation")
            history_icon = QLabel("▣")
            history_icon.setObjectName("conversationIcon")
            history_icon.setFixedSize(18, 24)
            history_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

            button = QPushButton(title)
            button.setObjectName("conversationItem")
            button.setProperty(
                "active",
                conversation.get("id") == self.chat.active_conversation_id,
            )
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setToolTip(title)
            button.setMinimumWidth(0)
            button.setMaximumWidth(160)
            button.setSizePolicy(
                 QSizePolicy.Policy.Ignored,
                QSizePolicy.Policy.Fixed,
            )
            button.clicked.connect(
                lambda checked=False, conversation_id=conversation.get("id"):
                self.chat.load_conversation(conversation_id)
            )

            timestamp = QLabel(detail)
            timestamp.setObjectName("conversationTime")
            timestamp.setFixedWidth(54)
            timestamp.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )

            menu_button = QPushButton("•••")
            menu_button.setObjectName("conversationMenuButton")
            menu_button.setFixedSize(28, 28)
            menu_button.setToolTip("Conversation actions")
            menu_button.setAccessibleName("Conversation actions")
            menu_button.clicked.connect(
                lambda checked=False, source=menu_button,
                conversation_id=conversation.get("id"):
                self.show_conversation_menu(source, conversation_id)
            )

            row_layout.addWidget(history_icon, 0, Qt.AlignmentFlag.AlignVCenter)
            row_layout.addWidget(button, 1)
            row_layout.addWidget(timestamp, 0)
            row_layout.addWidget(menu_button, 0)
            self.conversation_list.addWidget(row)

        self.conversation_list.addStretch()

    def show_conversation_menu(self, button, conversation_id):
        menu = QMenu(self)
        menu.setObjectName("conversationMenu")

        rename_action = menu.addAction("Rename")
        duplicate_action = menu.addAction("Duplicate")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")
        delete_action.setObjectName("deleteConversationAction")

        rename_action.triggered.connect(
            lambda: self.rename_conversation(conversation_id)
        )
        duplicate_action.triggered.connect(
            lambda: self.duplicate_conversation(conversation_id)
        )
        delete_action.triggered.connect(
            lambda: self.confirm_delete_conversation(conversation_id)
        )
        menu.popup(button.mapToGlobal(button.rect().bottomLeft()))

    def rename_conversation(self, conversation_id):
        conversation = next(
            (
                item for item in self.chat.conversations
                if item.get("id") == conversation_id
            ),
            None,
        )
        if conversation is None:
            return

        title, accepted = QInputDialog.getText(
            self,
            "Rename conversation",
            "Conversation title:",
            text=conversation.get("title", ""),
        )
        if accepted and not self.chat.rename_conversation(conversation_id, title):
            if title.strip():
                self.show_conversation_error(
                    "Could not rename this conversation."
                )

    def duplicate_conversation(self, conversation_id):
        if self.chat.duplicate_conversation(conversation_id) is None:
            self.show_conversation_error("Could not duplicate this conversation.")


    def confirm_delete_conversation(self, conversation_id):
        dialog = QMessageBox(self)
        dialog.setObjectName("deleteConversationDialog")
        dialog.setWindowTitle("Delete conversation?")
        dialog.setText(
            "This conversation and its saved messages will be permanently "
            "deleted. This action cannot be undone."
        )
        dialog.setIcon(QMessageBox.Icon.Warning)

        cancel = dialog.addButton(
            "Cancel",
            QMessageBox.ButtonRole.RejectRole,
        )
        delete = dialog.addButton(
            "Delete",
            QMessageBox.ButtonRole.DestructiveRole,
        )
        dialog.setDefaultButton(cancel)
        dialog.exec()

        if dialog.clickedButton() != delete:
            return
        print("DEBUG: Delete confirmed for:", conversation_id)

        
        result = self.chat.delete_conversation(conversation_id)
        print("DEBUG: Delete result:", result)
        if not result:
            self.show_conversation_error(
                "Could not delete this conversation. "
                "Check whether the conversation file is writable."
            )
            return

        self.refresh_conversation_history()

    def show_conversation_error(self, message):
        QMessageBox.warning(self, "Conversation history", message)

    def create_header(self):
        header = QFrame()
        header.setObjectName("topbar")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(2, 0, 2, 0)

        title_group = QVBoxLayout()
        title_group.setSpacing(4)

        self.page_title = QLabel("Chat")
        self.page_title.setObjectName("pageTitle")

        self.page_subtitle = QLabel(
            "Your personal AI workspace."
        )
        self.page_subtitle.setObjectName("muted")

        title_group.addWidget(self.page_title)
        title_group.addWidget(self.page_subtitle)

        layout.addLayout(title_group)
        layout.addStretch()

        version = QLabel("V3.0")
        version.setObjectName("version")
        layout.addWidget(version)

        return header

    def create_chat_page(self):
        page = QWidget()
        page.setObjectName("chatPage")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.chat = ChatWidget()
        layout.addWidget(self.chat)

        return page

    def create_right_panel(self):
        panel = QFrame()
        panel.setObjectName("rightPanel")
        panel.setFixedWidth(280)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 24, 16, 18)
        layout.setSpacing(11)

        heading = QLabel("Workspace")
        heading.setObjectName("panelTitle")

        subtitle = QLabel("Your connected capabilities")
        subtitle.setObjectName("muted")
        subtitle.setWordWrap(True)

        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addSpacing(8)

        layout.addWidget(
            self.create_info_card(
                "✦",
                "Local AI",
                "Qwen 2.5 3B through Ollama",
            )
        )

        layout.addWidget(
            self.create_info_card(
                "⌘",
                "Applications",
                "Launch supported Mac applications",
            )
        )

        layout.addWidget(
            self.create_info_card(
                "▤",
                "Files",
                "Search, read, create and edit files",
            )
        )

        layout.addWidget(
            self.create_info_card(
                "⌕",
                "Web",
                "Search the web and open webpages",
            )
        )

        layout.addWidget(
            self.create_info_card(
                "◇",
                "Memory",
                "Persistent memory system",
            )
        )

        layout.addWidget(
            self.create_info_card(
                "◉",
                "Vision",
                "Analyze screenshots and images",
            )
        )

        layout.addStretch()
        layout.addWidget(self.create_system_status_card())

        return panel

    def create_info_card(self, symbol, title, description):
        card = QFrame()
        card.setObjectName("infoCard")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 11, 11, 11)
        layout.setSpacing(10)

        icon = QLabel(symbol)
        icon.setObjectName("infoIcon")
        icon.setFixedSize(36, 36)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_group = QVBoxLayout()
        text_group.setSpacing(4)

        heading = QLabel(title)
        heading.setObjectName("infoTitle")

        body = QLabel(description)
        body.setObjectName("infoDescription")
        body.setWordWrap(True)

        text_group.addWidget(heading)
        text_group.addWidget(body)

        layout.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(text_group, 1)

        chevron = QLabel("›")
        chevron.setObjectName("infoChevron")
        chevron.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(chevron)

        return card

    def create_system_status_card(self):
        card = QFrame()
        card.setObjectName("systemStatus")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 11)
        layout.setSpacing(7)

        title_row = QHBoxLayout()
        title = QLabel("System Status")
        title.setObjectName("systemStatusTitle")
        state = QLabel("● Configured")
        state.setObjectName("systemStatusState")
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(state)
        layout.addLayout(title_row)

        for label, value in [
            ("Model", "Qwen 2.5 3B"),
            ("Provider", "Ollama (Local)"),
            ("Voice", "Available"),
            ("Memory", "Available"),
            ("Tools", "Available"),
        ]:
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            name = QLabel(label)
            name.setObjectName("statusRowLabel")
            detail = QLabel(value)
            detail.setObjectName("statusRowValue")
            row.addWidget(name)
            row.addStretch()
            row.addWidget(detail)
            layout.addLayout(row)

        return card

    def create_scroll_page(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("pageScroll")

        content = QWidget()
        content.setObjectName("pageContent")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        scroll.setWidget(content)

        return scroll, layout

    def create_info_page_card(self, title, description, tag):
        card = QFrame()
        card.setObjectName("pageCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        label = QLabel(tag.upper())
        label.setObjectName("cardTag")

        heading = QLabel(title)
        heading.setObjectName("cardTitle")

        body = QLabel(description)
        body.setObjectName("muted")
        body.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(heading)
        layout.addWidget(body)

        return card

    def create_memory_page(self):
        scroll, layout = self.create_scroll_page()

        layout.addWidget(
            self.create_info_page_card(
                "Persistent memory",
                "IRIS has an existing memory system. "
                "A full memory browser and editing interface "
                "still need to be connected.",
                "Memory",
            )
        )

        layout.addStretch()
        return scroll

    def create_tools_page(self):
        scroll, layout = self.create_scroll_page()

        cards = [
            (
                "File operations",
                "Search, read, create and edit files.",
                "FILES",
            ),
            (
                "Web browsing",
                "Search the web and open webpages.",
                "WEB",
            ),
            (
                "Application control",
                "Launch supported applications on your Mac.",
                "APPLICATIONS",
            ),
            (
                "System information",
                "Inspect available system information.",
                "SYSTEM",
            ),
            (
                "Vision",
                "Analyze screenshots and supplied images.",
                "VISION",
            ),
            (
                "Permissions",
                "Control access to supported actions.",
                "SECURITY",
            ),
        ]

        for title, description, tag in cards:
            layout.addWidget(
                self.create_info_page_card(
                    title,
                    description,
                    tag,
                )
            )

        layout.addStretch()
        return scroll

    def create_activity_page(self):
        scroll, layout = self.create_scroll_page()

        layout.addWidget(
            self.create_info_page_card(
                "Runtime diagnostics",
                "Use the existing test suite and health checks "
                "to verify the model, vision, memory and tools.",
                "DIAGNOSTICS",
            )
        )

        layout.addWidget(
            self.create_info_page_card(
                "Activity history",
                "A live searchable history of tool calls has "
                "not yet been connected to this page.",
                "STATUS",
            )
        )

        layout.addStretch()
        return scroll

    def navigate(self, name):
        page = self.pages.get(name)

        if page is None:
            return

        self.stack.setCurrentWidget(page)
        self.page_title.setText(name)

        subtitles = {
            "Chat": "Your personal AI workspace.",
            "Memory": "Information stored by IRIS.",
            "Tools": "Capabilities available to IRIS.",
            "Activity": "Runtime information and diagnostics.",
        }

        self.page_subtitle.setText(subtitles.get(name, ""))

        self.right_panel.setVisible(False)

        for page_name, button in self.nav_buttons.items():
            button.setProperty("active", page_name == name)
            button.style().unpolish(button)
            button.style().polish(button)

    def closeEvent(self, event):
        if self.chat.shutdown_workers():
            event.accept()
        else:
            event.ignore()

    def stylesheet(self):
        return """
        QMainWindow, QWidget#root {
            background: #17191C;
            color: #F1F3F5;
            font-family: "Helvetica Neue", Arial;
            font-size: 13px;
        }

        QWidget#workspace {
            background: #17191C;
        }

        QFrame#sidebar {
            background: #1C1F24;
            border-right: 1px solid #2C3036;
        }

        QLabel#logo {
            background: #087BE6;
            color: #FFFFFF;
            border-radius: 16px;
            font-size: 35px;
            font-weight: bold;
        }

        QLabel#brand {
            color: #F1F3F5;
            font-size: 25px;
            font-weight: 800;
            letter-spacing: 1px;
        }

        QLabel#eyebrow, QLabel#sectionLabel, QLabel#footer {
            color: #90959D;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        QPushButton#navButton {
            text-align: left;
            padding: 0 12px;
            background: transparent;
            color: #C8D1DD;
            border: none;
            border-radius: 9px;
            font-size: 14px;
            font-weight: 600;
        }

        QPushButton#navButton:hover {
            background: #292D33;
            color: #F1F3F5;
            border: none;
        }

        QPushButton#navButton[active="true"] {
            background: #183D67;
            color: #F1F3F5;
            border: 1px solid #246AAE;
        }

        QPushButton#navButton[active="true"]:hover {
            background: #2B4058;
            border: none;
        }

        QPushButton#navButton:focus {
            border: 1px solid #526274;
        }

        QFrame#statusCard, QFrame#pageCard, QFrame#systemStatus {
            background: #162231;
            border: 1px solid #314258;
            border-radius: 12px;
        }

        QLabel#statusTitle {
            color: #F4F7FC;
            font-size: 18px;
            font-weight: 700;
        }

        QLabel#muted {
            color: #A4ABB5;
            font-size: 12px;
        }

        QLabel#pageTitle {
            color: #F1F3F5;
            font-size: 30px;
            font-weight: 700;
        }

        QLabel#version {
            background: #162231;
            color: #D2DBE8;
            border: 1px solid #314258;
            border-radius: 12px;
            padding: 16px 18px;
            font-size: 14px;
            font-weight: 700;
        }

        QFrame#rightPanel {
            background: #1B1E23;
            border-left: 1px solid #303640;
        }

        QLabel#panelTitle {
            color: #F4F7FC;
            font-size: 19px;
            font-weight: 700;
        }

        QFrame#infoCard {
            background: #20242A;
            border: 1px solid #303640;
            border-radius: 8px;
        }

        QLabel#infoIcon {
            background: #2B313A;
            color: #C7CDD5;
            border-radius: 7px;
            font-size: 17px;
            font-weight: bold;
        }

        QLabel#infoTitle {
            color: #F4F7FC;
            font-size: 12px;
            font-weight: 700;
        }

        QLabel#infoDescription {
            color: #A4ABB5;
            font-size: 10px;
        }

        QLabel#panelNote {
            color: #64748B;
            font-size: 10px;
        }

        QFrame#sidebarDivider {
            color: #303640;
            background: #303640;
            max-height: 1px;
        }

        QLineEdit#conversationSearch {
            background: transparent;
            color: #D7DBE0;
            border: none;
            border-bottom: 1px solid #34475D;
            border-radius: 0;
            padding: 4px 2px;
            font-size: 12px;
        }

        QLineEdit#conversationSearch:focus {
            border-bottom: 1px solid #579FFF;
        }

        QScrollArea#conversationScroll, QWidget#conversationContent {
            background: transparent;
            border: none;
        }

        QPushButton#newChatButton {
            background: #18293A;
            color: #D7DBE0;
            border: 1px solid #31465F;
            border-radius: 12px;
            padding: 0 12px;
            text-align: left;
            font-size: 14px;
            font-weight: 700;
        }

        QPushButton#newChatButton:hover {
            background: #20354A;
            border: 1px solid #4B6A89;
        }

        QLabel#conversationEmpty {
            color: #78818D;
            font-size: 11px;
            padding: 0 9px;
        }

        QLabel#conversationGroup {
            color: #7D8590;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.8px;
            margin: 5px 6px 2px;
        }

        QLabel#conversationIcon {
            color: #9BA9BB;
            font-size: 14px;
        }

        QPushButton#conversationItem {
            background: transparent;
            color: #BEC5CD;
            border: 1px solid transparent;
            border-radius: 8px;
            padding: 4px 6px;
            text-align: left;
            font-size: 12px;
        }

        QPushButton#conversationItem:hover {
            background: #292D33;
            color: #F1F3F5;
        }

        QPushButton#conversationItem[active="true"] {
            background: #26394F;
            color: #F1F3F5;
            border: 1px solid #324C69;
        }

        QFrame#conversationRow {
            background: transparent;
            border: none;
            min-height: 29px;
        }

        QPushButton#conversationMenuButton {
            background: transparent;
            color: #BEC5CD;
            border: 1px solid transparent;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 700;
            padding: 0;
        }

        QPushButton#conversationMenuButton:hover {
            background: #303944;
            color: #FFFFFF;
            border: 1px solid #40546A;
        }

        QLabel#conversationTime {
            color: #78818D;
            font-size: 10px;
        }


        QLabel#statusModel {
            color: #31C48D;
            font-size: 10px;
            font-weight: 600;
        }

        QLabel#infoChevron {
            color: #78818D;
            font-size: 25px;
        }

        QFrame#infoCard:hover {
            background: #272D35;
            border: 1px solid #3A414C;
        }

        QLabel#systemStatusTitle {
            color: #F4F7FC;
            font-size: 12px;
            font-weight: 700;
        }

        QLabel#systemStatusState {
            color: #A4ABB5;
            font-size: 10px;
        }

        QLabel#statusRowLabel {
            color: #78818D;
            font-size: 10px;
        }

        QLabel#statusRowValue {
            color: #C7CDD5;
            font-size: 10px;
        }

        QLabel#cardTag {
            color: #93B4FF;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
        }

        QLabel#cardTitle {
            color: #F1F5F9;
            font-size: 16px;
            font-weight: 700;
        }

        QScrollArea#pageScroll, QWidget#pageContent {
            background: transparent;
            border: none;
        }
        """

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = IRISWindow()
    window.show()
    sys.exit(app.exec())
