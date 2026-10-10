from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def search(self, query, limit=5, topic_aware=False):
        return [
            {
                "role": "user",
                "content": "Yesterday I attended an AI workshop.",
                "score": 3
            },
            {
                "role": "user",
                "content": "Python is a programming language.",
                "score": 3
            },
            {
                "role": "user",
                "content": "Last week I completed a Python course.",
                "score": 3
            }
        ]


def main():
    reasoning = MemoryReasoning(FakeConversation())

    episodic = reasoning.retrieve_evidence(
        query="Python AI",
        limit=5,
        memory_type="episodic"
    )

    assert episodic["count"] > 0
    assert all(
        memory["memory_type"] == "episodic"
        for memory in episodic["memories"]
    )

    semantic = reasoning.retrieve_evidence(
        query="Python AI",
        limit=5,
        memory_type="semantic"
    )

    assert semantic["count"] > 0
    assert all(
        memory["memory_type"] == "semantic"
        for memory in semantic["memories"]
    )

    print("MEMORY TYPE RETRIEVAL TEST: PASS")


if __name__ == "__main__":
    main()
