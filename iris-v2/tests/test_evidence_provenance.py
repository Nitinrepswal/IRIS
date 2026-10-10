
from core.memory_reasoning_pipeline import MemoryReasoningPipeline


class FakeConversation:
    def search(self, query, limit=5, topic_aware=True):
        return [
            {
                "role": "user",
                "content": "The project uses SQLite.",
                "score": 3
            },
            {
                "role": "assistant",
                "content": "SQLite is an embedded database.",
                "score": 2
            }
        ][:limit]


def main():
    pipeline = MemoryReasoningPipeline(FakeConversation())
    result = pipeline.analyze("SQLite")

    assert result["evidence_count"] == 2
    assert len(result["sources"]) == 2

    for evidence, source in zip(
        result["evidence"],
        result["sources"]
    ):
        assert evidence["source_index"] == source["source_index"]
        assert evidence["role"] == source["role"]
        assert evidence["score"] == source["score"]
        assert source["source"]["type"] == (
            "conversation_search_result"
        )
        assert source["source"]["result_index"] == (
            source["source_index"]
        )

    assert result["status"] == "evidence_found"

    print("EVIDENCE PROVENANCE TEST: PASS")


if __name__ == "__main__":
    main()
