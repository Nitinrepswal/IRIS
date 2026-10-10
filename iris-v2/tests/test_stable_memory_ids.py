
from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def __init__(self, results):
        self.results = results

    def search(self, query, limit=5, topic_aware=True):
        return self.results[:limit]


def main():
    first_results = [
        {
            "role": "user",
            "content": "The project uses SQLite.",
            "score": 3
        },
        {
            "role": "assistant",
            "content": "Python supports functions.",
            "score": 2
        }
    ]

    reordered_results = list(reversed(first_results))

    first = MemoryReasoning(
        FakeConversation(first_results)
    ).retrieve_evidence("project")

    reordered = MemoryReasoning(
        FakeConversation(reordered_results)
    ).retrieve_evidence("project")

    first_ids = {
        item["content"]: item["memory_id"]
        for item in first["memories"]
    }

    reordered_ids = {
        item["content"]: item["memory_id"]
        for item in reordered["memories"]
    }

    assert first_ids == reordered_ids

    for item in first["memories"]:
        assert item["memory_id"].startswith("mem_")
        assert item["source"]["memory_id"] == item["memory_id"]

    changed = MemoryReasoning(
        FakeConversation([
            {
                "role": "user",
                "content": "The project uses PostgreSQL.",
                "score": 3
            }
        ])
    ).retrieve_evidence("project")

    assert (
        first_ids["The project uses SQLite."]
        != changed["memories"][0]["memory_id"]
    )

    print("STABLE MEMORY IDS TEST: PASS")


if __name__ == "__main__":
    main()
