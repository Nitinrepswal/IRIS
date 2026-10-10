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
            }
        ]


def main():
    reasoning = MemoryReasoning(FakeConversation())

    result = reasoning.retrieve_evidence(
        query="Python AI workshop",
        limit=5
    )

    assert result["count"] == 2

    for memory in result["memories"]:
        assert memory["memory_type"] in (
            "episodic",
            "semantic"
        )

    types = {
        memory["content"]: memory["memory_type"]
        for memory in result["memories"]
    }

    assert types["Yesterday I attended an AI workshop."] == "episodic"
    assert types["Python is a programming language."] == "semantic"

    print("MEMORY TYPES TEST: PASS")


if __name__ == "__main__":
    main()
