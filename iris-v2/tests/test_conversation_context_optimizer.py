
from core.conversation_context_optimizer import ConversationContextOptimizer


def main():
    optimizer = ConversationContextOptimizer(max_characters=100)

    messages = [
        {
            "role": "user",
            "content": "Python is a programming language.",
            "score": 1
        },
        {
            "role": "assistant",
            "content": "Database indexing improves query performance.",
            "score": 3,
            "topic_score": 2
        },
        {
            "role": "user",
            "content": "Python is a programming language.",
            "score": 1
        },
        {
            "role": "assistant",
            "content": "Database indexing is useful.",
            "score": 2
        }
    ]

    result = optimizer.optimize(messages)

    assert result["count"] >= 1
    assert result["character_count"] == len(result["context"])
    assert result["character_count"] <= 100

    contents = [
        message["content"].lower()
        for message in result["messages"]
    ]

    assert len(contents) == len(set(contents))
    assert result["messages"][0]["content"] == (
        "Database indexing improves query performance."
    )

    small_optimizer = ConversationContextOptimizer(max_characters=20)
    small_result = small_optimizer.optimize(messages)

    assert small_result["character_count"] <= 20
    assert small_result["character_count"] == len(
        small_result["context"]
    )

    empty_result = optimizer.optimize([])

    assert empty_result["context"] == ""
    assert empty_result["count"] == 0
    assert empty_result["character_count"] == 0

    try:
        optimizer.optimize("invalid")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid messages should be rejected")

    try:
        ConversationContextOptimizer(max_characters=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid character limit should be rejected")

    print("CONVERSATION CONTEXT OPTIMIZER TEST: PASS")


if __name__ == "__main__":
    main()
