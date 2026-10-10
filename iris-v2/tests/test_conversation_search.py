
from core.conversation_search import ConversationSearch


def main():
    search = ConversationSearch()

    messages = [
        {
            "role": "user",
            "content": "Tell me about Python programming."
        },
        {
            "role": "assistant",
            "content": "Python is a popular programming language."
        },
        {
            "role": "user",
            "content": "Explain database indexing."
        },
        {
            "role": "assistant",
            "content": "Database indexing improves query performance."
        },
        {
            "role": "user",
            "content": "What is Python database integration?"
        },
        {
            "role": "assistant",
            "content": "Database indexing is important."
        }
    ]

    # Single keyword search
    results = search.search("python", messages)

    assert len(results) == 3
    assert all(
        "python" in item["content"].lower()
        for item in results
    )

    # Exact phrase matching
    results = search.search("database indexing", messages)

    assert results[0]["phrase_match"] is True
    assert results[0]["score"] == 2
    assert "database indexing" in results[0]["content"].lower()

    # Database appears in four messages
    results = search.search("database", messages)

    assert len(results) == 4
    assert all(item["score"] == 1 for item in results)

    # Multiword query ranking
    results = search.search("python database", messages)

    assert results[0]["phrase_match"] is True
    assert results[0]["score"] == 2

    # Duplicate query words must not inflate scores
    duplicate_results = search.search("python python", messages)

    assert len(duplicate_results) == 3
    assert all(item["score"] == 1 for item in duplicate_results)

    # Case-insensitive search
    results = search.search("PYTHON", messages)

    assert len(results) == 3

    # Result limit
    results = search.search("python", messages, limit=1)

    assert len(results) == 1

    # Empty and irrelevant queries
    assert search.search("", messages) == []
    assert search.search("   ", messages) == []
    assert search.search("quantum physics", messages) == []

    # Invalid limit
    try:
        search.search("python", messages, limit=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid limit should be rejected")

    # Invalid messages
    try:
        search.search("python", "not a message list")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid messages should be rejected")

    print("CONVERSATION SEARCH V2 TEST: PASS")


if __name__ == "__main__":
    main()
