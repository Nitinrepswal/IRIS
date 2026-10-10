
import json
import os
import tempfile

from core.memory_reasoning import MemoryReasoning
from core.persistent_conversation import PersistentConversation


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "context.json")

        conversation = PersistentConversation(path=path)
        conversation.intelligence.add_user_message(
            "Yesterday I completed my Python project."
        )
        conversation.save()

        with open(path, encoding="utf-8") as file:
            saved = json.load(file)

        saved_message = saved["context"]["messages"][0]
        assert isinstance(saved_message["timestamp"], (int, float))

        restored = PersistentConversation(path=path)
        assert restored.load() is True

        restored_message = restored.intelligence.state.messages[0]
        assert restored_message["timestamp"] == saved_message["timestamp"]

        reasoning = MemoryReasoning(restored)
        result = reasoning.retrieve_evidence(
            query="Python project",
            limit=5
        )

        assert result["count"] > 0

        memory = result["memories"][0]
        assert memory["timestamp"] == saved_message["timestamp"]
        assert memory["memory_type"] == "episodic"
        assert 0.0 <= memory["importance_score"] <= 1.0

        print("TIMESTAMP PERSISTENCE: PASS")
        print("MEMORY TYPE AFTER RESTORE: PASS")
        print("IMPORTANCE AFTER RESTORE: PASS")


if __name__ == "__main__":
    main()
