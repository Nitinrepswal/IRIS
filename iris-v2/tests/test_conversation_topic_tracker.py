from core.conversation_topic_tracker import ConversationTopicTracker


def main():
    tracker = ConversationTopicTracker()

    result = tracker.update("Tell me about Python.")
    assert result["type"] == "new_topic"
    assert tracker.get_topic() == "Python"

    result = tracker.update("What are its uses?")
    assert result["type"] == "follow_up"
    assert tracker.get_topic() == "Python"

    result = tracker.update("Explain database indexing.")
    assert result["type"] == "new_topic"
    assert tracker.get_topic() == "database indexing"
    assert result["topic_changes"] == 1

    result = tracker.update("   ")
    assert result["updated"] is False
    assert tracker.get_topic() == "database indexing"

    tracker.clear()
    assert tracker.get_topic() == ""
    assert tracker.history == []
    assert tracker.topic_changes == 0

    print("CONVERSATION TOPIC TRACKER TEST: PASS")


if __name__ == "__main__":
    main()
