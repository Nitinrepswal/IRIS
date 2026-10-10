
import tempfile
from pathlib import Path

from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def search(self, query, limit=5, topic_aware=False):
        return [
            {
                "role": "user",
                "content": "My project is IRIS, an AI assistant.",
                "score": 3,
                "timestamp": 1791638400
            },
            {
                "role": "user",
                "content": "I attended an AI workshop yesterday.",
                "score": 2,
                "timestamp": 1791638400
            },
            {
                "role": "assistant",
                "content": "Python is a programming language.",
                "score": 1,
                "timestamp": 1791638400
            }
        ]


def main():
    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        reasoning = MemoryReasoning(FakeConversation())

        result = reasoning.retrieve_evidence(
            query="AI Python project",
            limit=5
        )

        assert result["count"] == 3

        memories = result["memories"]

        for memory in memories:
            assert memory["memory_id"].startswith("mem_")
            assert memory["memory_type"] in {"episodic", "semantic"}
            assert "importance_score" in memory
            assert "importance_feedback" in memory
            assert "privacy" in memory
            assert "source" in memory

        target = next(
            memory for memory in memories
            if memory["content"].startswith("My project is IRIS")
        )
        memory_id = target["memory_id"]

        reasoning.set_importance_feedback(memory_id, "important")
        reasoning.set_memory_privacy(
            memories[1]["memory_id"], "private"
        )

        feedback_path = directory / "feedback.json"
        privacy_path = directory / "privacy.json"

        reasoning.save_importance_feedback(feedback_path)
        reasoning.save_memory_privacy(privacy_path)

        restored = MemoryReasoning(FakeConversation())
        restored.load_importance_feedback(feedback_path)
        restored.load_memory_privacy(privacy_path)

        assert restored.get_importance_feedback(memory_id) == "important"
        assert restored.get_memory_privacy(memories[1]["memory_id"]) == "private"

        final_result = restored.retrieve_evidence(
            query="AI Python project",
            limit=5
        )

        assert final_result["count"] == 2
        assert all(
            memory["memory_id"] != memories[1]["memory_id"]
            for memory in final_result["memories"]
        )

        final_target = next(
            memory for memory in final_result["memories"]
            if memory["memory_id"] == memory_id
        )
        assert final_target["importance_feedback"] == "important"

        package = restored.build_answer_package(
            query="AI Python project",
            limit=5
        )
        assert package["answer_ready"] is True
        assert package["evidence_count"] == 2
        assert all(
            source["memory_id"] != memories[1]["memory_id"]
            for source in package["sources"]
        )

    print("MEMORY V3 INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()
