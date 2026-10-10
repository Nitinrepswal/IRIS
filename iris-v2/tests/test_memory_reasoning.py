
from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def search(self, query, limit=5, topic_aware=True):
        results = [
            {
                "role": "user",
                "content": "Python supports functions.",
                "score": 2
            },
            {
                "role": "assistant",
                "content": "Functions are reusable blocks of code.",
                "score": 1
            },
            {
                "role": "user",
                "content": "An unrelated low-score memory.",
                "score": 0
            }
        ]

        return results[:limit]


def main():
    reasoning = MemoryReasoning(FakeConversation())

    result = reasoning.retrieve_evidence("Python functions")

    assert result["query"] == "Python functions"
    assert result["count"] == 3
    assert result["memories"][0]["score"] == 2
    assert result["memories"][0]["source_index"] == 0

    filtered = reasoning.retrieve_evidence(
        "Python functions",
        min_score=1
    )
    assert filtered["count"] == 2

    package = reasoning.build_answer_package("Python functions")

    assert package["status"] == "evidence_found"
    assert package["answer_ready"] is True
    assert package["evidence_count"] == 3
    assert len(package["sources"]) == 3
    assert package["sources"][0]["role"] == "user"

    empty = reasoning.build_answer_package(
        "unknown topic",
        min_score=100
    )
    assert empty["status"] == "insufficient_evidence"
    assert empty["answer_ready"] is False
    assert empty["evidence_count"] == 0
    assert len(empty["limitations"]) > 0

    try:
        reasoning.retrieve_evidence("Python", limit=0)
        raise AssertionError("Invalid limit was accepted")
    except ValueError:
        pass

    print("MEMORY REASONING V3 TEST: PASS")


if __name__ == "__main__":
    main()
