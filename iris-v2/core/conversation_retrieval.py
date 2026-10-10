
class ConversationRetrieval:
    def __init__(self, conversation):
        self.conversation = conversation

    def retrieve(self, query, limit=5, topic_aware=True):
        if not isinstance(query, str) or not query.strip():
            return {
                "query": query if isinstance(query, str) else "",
                "topic": "",
                "messages": [],
                "count": 0
            }

        results = self.conversation.search_history(
            query=query,
            limit=limit,
            topic_aware=topic_aware
        )

        topic = self.conversation.intelligence.topic_tracker.get_topic()

        return {
            "query": query,
            "topic": topic,
            "messages": results,
            "count": len(results)
        }
