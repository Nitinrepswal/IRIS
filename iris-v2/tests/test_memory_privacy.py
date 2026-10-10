
from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def search(self, query, limit=5, topic_aware=False):
        return [
            {
                "role": "user",
                "content": "Python is a programming language.",
                "score": 2
            },
            {
                "role": "user",
                "content": "I attended an AI workshop yesterday.",
                "score": 2
            }
        ]


def main():
    reasoning = MemoryReasoning(FakeConversation())

    initial = reasoning.retrieve_evidence(
        query="Python AI workshop",
        limit=5
    )
    assert initial["count"] == 2

    memory_id = initial["memories"][0]["memory_id"]

    reasoning.set_memory_privacy(memory_id, "private")

    private_results = reasoning.retrieve_evidence(
        query="Python AI workshop",
        limit=5
    )

    assert all(
        memory["memory_id"] != memory_id
        for memory in private_results["memories"]
    )

    reasoning.set_memory_privacy(memory_id, "excluded")

    excluded_results = reasoning.retrieve_evidence(
        query="Python AI workshop",
        limit=5
    )

    assert all(
        memory["memory_id"] != memory_id
        for memory in excluded_results["memories"]
    )

    reasoning.set_memory_privacy(memory_id, "normal")

    restored_results = reasoning.retrieve_evidence(
        query="Python AI workshop",
        limit=5
    )

    assert any(
        memory["memory_id"] == memory_id
        for memory in restored_results["memories"]
    )

    print("MEMORY PRIVACY TEST: PASS")


if __name__ == "__main__":
    main()
