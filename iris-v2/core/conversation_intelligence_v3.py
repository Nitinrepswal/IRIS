
import json
import os

from core.persistent_conversation import PersistentConversation
from core.conversation_retrieval import ConversationRetrieval
from core.context_window_builder import ContextWindowBuilder
from core.conversation_context_optimizer import ConversationContextOptimizer
from core.conversation_flow_manager import ConversationFlowManager


class ConversationIntelligenceV3:
    def __init__(
        self,
        path="memory/intelligence_context.json",
        max_messages=20,
        max_characters=6000,
        context_budget=3000
    ):
        self.conversation = PersistentConversation(
            path=path,
            max_messages=max_messages,
            max_characters=max_characters
        )

        self.flow_path = path + ".flow.json"

        self.retrieval = ConversationRetrieval(self.conversation)

        self.context_builder = ContextWindowBuilder(
            self.retrieval,
            max_characters=context_budget
        )

        self.optimizer = ConversationContextOptimizer(
            max_characters=context_budget
        )

        self.flow_manager = ConversationFlowManager()

    def add_user_message(self, message):
        return self.conversation.intelligence.add_user_message(message)

    def add_assistant_message(self, message):
        return self.conversation.intelligence.add_assistant_message(message)

    def process_user_message(self, message):
        self.add_user_message(message)
        return self.flow_manager.process(message)

    def process_flow(self, message):
        return self.flow_manager.process(message)

    def get_flow_state(self):
        return self.flow_manager.get_state()

    def analyze_message(self, message):
        return self.conversation.intelligence.analyze_message(message)

    def search(self, query, limit=5, topic_aware=True):
        return self.conversation.search_history(
            query=query,
            limit=limit,
            topic_aware=topic_aware
        )

    def retrieve(self, query, limit=5, topic_aware=True):
        return self.retrieval.retrieve(
            query=query,
            limit=limit,
            topic_aware=topic_aware
        )

    def build_context(self, query, limit=5, topic_aware=True):
        result = self.context_builder.build(
            query=query,
            limit=limit,
            topic_aware=topic_aware
        )

        optimized = self.optimizer.optimize(result["messages"])

        return {
            "query": result["query"],
            "topic": result["topic"],
            "context": optimized["context"],
            "messages": optimized["messages"],
            "count": optimized["count"],
            "character_count": optimized["character_count"],
            "truncated": (
                result["truncated"] or optimized["truncated"]
            )
        }

    def get_context(self):
        return self.conversation.get_context()

    def save(self):
        self.conversation.save()

        directory = os.path.dirname(self.flow_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.flow_path, "w", encoding="utf-8") as file:
            json.dump(
                self.flow_manager.export_state(),
                file,
                indent=2,
                ensure_ascii=False
            )

    def _recover_flow_from_messages(self):
        self.flow_manager.clear()

        context = self.conversation.get_context()
        messages = context.get("messages", [])

        for message in messages:
            if not isinstance(message, dict):
                continue

            if message.get("role") != "user":
                continue

            content = message.get("content")

            if isinstance(content, str) and content.strip():
                self.flow_manager.process(content)

    def load(self):
        saved_flow = None

        if os.path.exists(self.flow_path):
            try:
                with open(self.flow_path, "r", encoding="utf-8") as file:
                    saved_flow = json.load(file)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise ValueError(
                    "Saved flow state is not valid JSON"
                ) from exc

            # Validate flow data before loading conversation data.
            flow_check = ConversationFlowManager()
            flow_check.restore_state(saved_flow)

        loaded = self.conversation.load()

        if not loaded:
            return False

        if saved_flow is not None:
            self.flow_manager.restore_state(saved_flow)
        else:
            self._recover_flow_from_messages()

        return True

    def clear(self):
        self.conversation.clear()
        self.flow_manager.clear()

        if os.path.exists(self.flow_path):
            os.remove(self.flow_path)
