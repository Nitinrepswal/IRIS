
from core.memory_reasoning_pipeline import MemoryReasoningPipeline


class FakeConversation:
    def __init__(self, results):
        self.results = results

    def search(self, query, limit=5, topic_aware=True):
        return self.results[:limit]


def main():
    conflicting_memories = [
        {
            "role": "user",
            "content": "The project uses SQLite.",
            "score": 3
        },
        {
            "role": "assistant",
            "content": "The project uses PostgreSQL.",
            "score": 2
        }
    ]

    pipeline = MemoryReasoningPipeline(
        FakeConversation(conflicting_memories)
    )

    result = pipeline.analyze("project database")

    assert result["status"] == "potential_conflict"
    assert result["answer_ready"] is False
    assert result["evidence_count"] == 2
    assert result["conflict_count"] == 1
    assert len(result["sources"]) == 2
    assert result["limitations"]

    empty_pipeline = MemoryReasoningPipeline(
        FakeConversation([])
    )

    empty = empty_pipeline.analyze("unknown topic")

    assert empty["status"] == "insufficient_evidence"
    assert empty["answer_ready"] is False
    assert empty["evidence_count"] == 0
    assert empty["conflict_count"] == 0

    consistent_pipeline = MemoryReasoningPipeline(
        FakeConversation([
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
        ])
    )

    consistent = consistent_pipeline.analyze("project")

    assert consistent["status"] == "evidence_found"
    assert consistent["answer_ready"] is True
    assert consistent["conflict_count"] == 0

    print("MEMORY REASONING PIPELINE TEST: PASS")


if __name__ == "__main__":
    main()
