
import json
import tempfile
from pathlib import Path

from core.memory_reasoning import MemoryReasoning


class FakeConversation:
    def search(self, query, limit=5, topic_aware=False):
        return [
            {
                "role": "user",
                "content": "Python is a programming language.",
                "score": 2
            }
        ]


def main():
    with tempfile.TemporaryDirectory() as directory:
        feedback_path = Path(directory) / "memory_feedback.json"

        first = MemoryReasoning(FakeConversation())

        memory = first.retrieve_evidence(
            query="Python",
            limit=5
        )["memories"][0]

        first.set_importance_feedback(
            memory["memory_id"],
            "important"
        )

        first.save_importance_feedback(feedback_path)

        assert feedback_path.exists()

        stored = json.loads(feedback_path.read_text())
        assert stored[memory["memory_id"]] == "important"

        second = MemoryReasoning(FakeConversation())
        second.load_importance_feedback(feedback_path)

        restored = second.retrieve_evidence(
            query="Python",
            limit=5
        )["memories"][0]

        assert restored["importance_feedback"] == "important"

    print("MEMORY FEEDBACK PERSISTENCE TEST: PASS")


if __name__ == "__main__":
    main()
