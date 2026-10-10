
from core.persistent_conversation import PersistentConversation
from core.conversation_retrieval import ConversationRetrieval
from core.context_window_builder import ContextWindowBuilder
from core.conversation_context_optimizer import ConversationContextOptimizer


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

        self.retrieval = ConversationRetrieval(self.conversation)

        self.context_builder = ContextWindowBuilder(
            self.retrieval,
            max_characters=context_budget
        )

        self.optimizer = ConversationContextOptimizer(
            max_characters=context_budget
        )

    def add_user_message(self, message):
        return self.conversation.intelligence.add_user_message(message)

    def add_assistant_message(self, message):
        return self.conversation.intelligence.add_assistant_message(message)

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

    def load(self):
        return self.conversation.load()

    def clear(self):
        self.conversation.clear()
