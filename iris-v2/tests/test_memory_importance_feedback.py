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

    for memory in initial["memories"]:
        assert "importance_score" in memory
        assert memory["importance_feedback"] == "neutral"

    target = initial["memories"][0]
    memory_id = target["memory_id"]
    original_score = target["ranking_score"]

    result = reasoning.set_importance_feedback(
        memory_id, "important"
    )
    assert result["importance_feedback"] == "important"

    updated = reasoning.retrieve_evidence(
        query="Python AI workshop",
        limit=5
    )
    selected = next(
        memory for memory in updated["memories"]
        if memory["memory_id"] == memory_id
    )

    assert selected["importance_feedback"] == "important"
    assert selected["ranking_score"] > original_score
    assert selected["importance_score"] == target["importance_score"]

    reasoning.set_importance_feedback(memory_id, "unimportant")
    updated = reasoning.retrieve_evidence(
        query="Python AI workshop",
        limit=5
    )
    selected = next(
        memory for memory in updated["memories"]
        if memory["memory_id"] == memory_id
    )
    assert selected["importance_feedback"] == "unimportant"
    assert selected["ranking_score"] < original_score

    reasoning.set_importance_feedback(memory_id, "neutral")
    assert reasoning.get_importance_feedback(memory_id) == "neutral"

    try:
        reasoning.set_importance_feedback(memory_id, "maybe")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid feedback should raise ValueError")

    print("MEMORY IMPORTANCE FEEDBACK TEST: PASS")


if __name__ == "__main__":
    main()
