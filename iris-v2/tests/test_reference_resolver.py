
from core.reference_resolver import ReferenceResolver


def main():
    resolver = ReferenceResolver()

    history = [
        {"role": "user", "content": "Tell me about Python."},
        {"role": "assistant", "content": "Python is a programming language."}
    ]

    result = resolver.resolve("What are its uses?", history)

    assert result["resolved"] is True
    assert result["subject"] == "Python"
    assert result["reference"] == "its"

    result = resolver.resolve("Explain its benefits.", history)

    assert result["resolved"] is True
    assert result["subject"] == "Python"

    result = resolver.resolve("Hello IRIS.", history)

    assert result["resolved"] is False

    result = resolver.resolve("What are its uses?", [])

    assert result["resolved"] is False

    result = resolver.resolve("   ", history)

    assert result["resolved"] is False

    print("REFERENCE RESOLVER TEST: PASS")


if __name__ == "__main__":
    main()

