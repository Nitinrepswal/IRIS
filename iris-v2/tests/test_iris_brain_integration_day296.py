
from core.iris_brain import IRISBrain


class FakeModel:
    def structured_chat(self, messages):
        prompt = messages[0]["content"]

        if "intent classifier" in prompt.lower():
            return {
                "intent": "filesystem",
                "reason": "The user wants to find a file.",
                "confidence": 0.95,
            }

        if "natural-language tool detector" in prompt.lower():
            return {
                "tool": "filesystem_search",
                "reason": "The user wants to find a file.",
            }

        raise AssertionError("Unexpected model prompt")

    def generate(self, message):
        return f"Fake response: {message}"

    def chat(self, messages):
        assert isinstance(messages, list)
        assert messages[0]["content"] == "Find my project files"
        return "Fake conversation response"


def main():
    brain = IRISBrain(FakeModel())

    result = brain.process("Find my project files")

    assert result["intent"] == "filesystem"
    assert result["tool"] == "filesystem_search"
    assert "understanding" in result
    assert result["response"] == "Fake conversation response"

    print("DAY 296 IRIS BRAIN INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()
