
from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def search(self, query, limit=5, topic_aware=True):
        results = [
            {
                "role": "user",
                "content": "Duplicate memory.",
                "score": 5
            },
            {
                "role": "user",
                "content": "Duplicate memory.",
                "score": 4
            },
            {
                "role": "user",
                "content": "Duplicate memory.",
                "score": 3
            },
            {
                "role": "assistant",
                "content": "Useful unique memory.",
                "score": 4
            },
            {
                "role": "user",
                "content": "Another useful memory.",
                "score": 2
            }
        ]

        assert limit >= len(results)
        return results


def main():
    reasoning = MemoryReasoning(FakeConversation())

    result = reasoning.retrieve_evidence(
        "memory",
        limit=3
    )

    assert result["count"] == 3

    contents = [item["content"] for item in result["memories"]]

    assert contents == [
        "Duplicate memory.",
        "Useful unique memory.",
        "Another useful memory."
    ]

    scores = [item["score"] for item in result["memories"]]
    assert scores == sorted(scores, reverse=True)

    ids = [item["memory_id"] for item in result["memories"]]
    assert len(ids) == len(set(ids))

    print("MEMORY RANKING TEST: PASS")


if __name__ == "__main__":
    main()
