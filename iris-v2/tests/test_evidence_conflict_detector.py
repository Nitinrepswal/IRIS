
from core.evidence_conflict_detector import EvidenceConflictDetector


def main():
    detector = EvidenceConflictDetector()

    memories = [
        {
            "content": "The project uses SQLite."
        },
        {
            "content": "The project uses PostgreSQL."
        },
        {
            "content": "Python supports functions."
        }
    ]

    result = detector.detect(memories)

    assert result["count"] == 1

    conflict = result["conflicts"][0]

    assert conflict["type"] == "technology"
    assert conflict["values"] == ["postgresql", "sqlite"]
    assert conflict["status"] == "potential_conflict"
    assert len(conflict["evidence"]) == 2

    assert conflict["evidence"][0]["content"] == (
        "The project uses SQLite."
    )
    assert conflict["evidence"][1]["content"] == (
        "The project uses PostgreSQL."
    )

    no_conflicts = detector.detect([
        {"content": "The project uses SQLite."},
        {"content": "The project uses SQLite."}
    ])

    assert no_conflicts["count"] == 0

    empty = detector.detect([])
    assert empty["count"] == 0

    try:
        detector.detect("not a list")
        raise AssertionError("Invalid input was accepted")
    except ValueError:
        pass

    print("EVIDENCE CONFLICT DETECTOR TEST: PASS")


if __name__ == "__main__":
    main()
