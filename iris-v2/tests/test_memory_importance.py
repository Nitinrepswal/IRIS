from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def search(self, query, limit=5, topic_aware=False):
        return [
            {
                "role": "user",
                "content": "My name is Nitin and this is important.",
                "score": 2
            },
            {
                "role": "user",
                "content": "I prefer C++ for coding interviews.",
                "score": 2
            },
            {
                "role": "assistant",
                "content": "Here is a simple Python example.",
                "score": 2
            }
        ]


def main():
    reasoning = MemoryReasoning(FakeConversation())

    result = reasoning.retrieve_evidence(
        query="coding",
        limit=5
    )

    assert result["count"] > 0

    for memory in result["memories"]:
        assert "importance_score" in memory
        assert 0.0 <= memory["importance_score"] <= 1.0

    important_memories = [
        memory
        for memory in result["memories"]
        if "my name is" in memory["content"].lower()
    ]

    assert important_memories
    assert important_memories[0]["importance_score"] > 0

    print("MEMORY IMPORTANCE TEST: PASS")


if __name__ == "__main__":
    main()
