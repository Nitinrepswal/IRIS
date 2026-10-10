
from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def __init__(self, results):
        self.results = results

    def search(self, query, limit=5, topic_aware=True):
        return self.results[:limit]


def main():
    results = [
        {
            "role": "user",
            "content": "The project uses SQLite.",
            "score": 3
        },
        {
            "role": "user",
            "content": "The project uses SQLite.",
            "score": 2
        },
        {
            "role": "assistant",
            "content": "The project uses SQLite.",
            "score": 2
        },
        {
            "role": "user",
            "content": "The project uses PostgreSQL.",
            "score": 1
        }
    ]

    reasoning = MemoryReasoning(FakeConversation(results))

    deduplicated = reasoning.retrieve_evidence(
        "project database",
        limit=5
    )

    assert deduplicated["count"] == 3

    ids = [item["memory_id"] for item in deduplicated["memories"]]
    assert len(ids) == len(set(ids))

    # The same text from different roles remains distinct.
    sqlite_memories = [
        item for item in deduplicated["memories"]
        if item["content"] == "The project uses SQLite."
    ]

    assert len(sqlite_memories) == 2
    assert {item["role"] for item in sqlite_memories} == {
        "user",
        "assistant"
    }

    # Disabling deduplication preserves duplicate search results.
    raw = reasoning.retrieve_evidence(
        "project database",
        limit=5,
        deduplicate=False
    )

    assert raw["count"] == 4

    print("MEMORY DEDUPLICATION TEST: PASS")


if __name__ == "__main__":
    main()
