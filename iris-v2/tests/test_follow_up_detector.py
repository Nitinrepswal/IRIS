
from core.follow_up_detector import FollowUpDetector


def main():
    detector = FollowUpDetector()

    history = [
        {"role": "user", "content": "Tell me about Python."},
        {"role": "assistant", "content": "Python is a programming language."}
    ]

    result = detector.detect("What are its uses?", history)
    assert result["type"] == "follow_up"

    result = detector.detect("Tell me more about it.", history)
    assert result["type"] == "follow_up"

    result = detector.detect("Explain database indexing.", history)
    assert result["type"] == "new_topic"

    result = detector.detect("Okay", history)
    assert result["type"] == "uncertain"

    result = detector.detect("Hello", [])
    assert result["type"] == "uncertain"

    result = detector.detect("", history)
    assert result["type"] == "uncertain"

    print("FOLLOW-UP DETECTOR TEST: PASS")


if __name__ == "__main__":
    main()

