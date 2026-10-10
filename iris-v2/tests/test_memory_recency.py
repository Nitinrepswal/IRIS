
import time

from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def search(self, query, limit=5, topic_aware=True):
        now = time.time()

        return [
            {
                "role": "user",
                "content": "Older relevant memory.",
                "score": 3,
                "timestamp": now - 90 * 86400
            },
            {
                "role": "user",
                "content": "Recent relevant memory.",
                "score": 3,
                "timestamp": now - 86400
            },
            {
                "role": "assistant",
                "content": "Memory with unknown timestamp.",
                "score": 3
            }
        ]


def main():
    reasoning = MemoryReasoning(FakeConversation())

    result = reasoning.retrieve_evidence("memory", limit=3)

    assert result["count"] == 3

    memories = result["memories"]

    assert memories[0]["content"] == "Recent relevant memory."
    assert memories[0]["recency_score"] > (
        next(
            item["recency_score"]
            for item in memories
            if item["content"] == "Older relevant memory."
        )
    )

    unknown = next(
        item for item in memories
        if item["content"] == "Memory with unknown timestamp."
    )
    assert unknown["recency_score"] == 0.0

    ranking_scores = [item["ranking_score"] for item in memories]
    assert ranking_scores == sorted(ranking_scores, reverse=True)

    print("MEMORY RECENCY TEST: PASS")


if __name__ == "__main__":
    main()
