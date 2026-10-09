
import importlib
from core.context_manager import ContextManager
from core.conversation_state import ConversationState
from core.response import IRISResponse
from models.llm_model import LLMModel


def main():
    print("IRIS V3.1 STABILITY RELEASE CHECK")
    print("=" * 55)

    results = []

    def check(name, function):
        try:
            function()
            results.append((name, True))
            print(f"PASS: {name}")
        except Exception as error:
            results.append((name, False))
            print(f"FAIL: {name} - {error}")

    def test_imports():
        modules = [
            "core.error_handler",
            "core.logger",
            "core.profiler",
            "core.tool_profiler",
            "core.response",
            "core.conversation_state",
            "core.context_manager",
            "core.intent",
            "models.llm_model",
        ]

        for module in modules:
            importlib.import_module(module)

    def test_context_limits():
        manager = ContextManager(
            max_messages=3,
            max_characters=20
        )

        messages = [
            {"role": "user", "content": "old message"},
            {"role": "assistant", "content": "older response"},
            {"role": "user", "content": "latest request"}
        ]

        result = manager.trim_messages(messages)

        assert len(result) <= 3
        assert manager.get_character_count(result) <= 20
        assert result[-1]["content"] == "latest request"

    def test_conversation_state():
        state = ConversationState()
        state.add_user_message("Hello")
        state.add_assistant_message("Hi")

        assert state.get_turn_count() == 1
        assert len(state.get_messages()) == 2
        assert state.get_context()["last_response"] == "Hi"

    def test_response():
        result = IRISResponse.success_response(
            "IRIS is ready",
            source="system"
        ).to_dict()

        assert result["success"] is True
        assert result["content"] == "IRIS is ready"

    def test_prompt():
        model = LLMModel()
        prompt = model.system_prompt

        assert "You are IRIS" in prompt
        assert "Nitin" in prompt
        assert "CAPABILITIES:" in prompt
        assert "BEHAVIOR:" in prompt

    check("Core module imports", test_imports)
    check("Context window limits", test_context_limits)
    check("Conversation state", test_conversation_state)
    check("Unified response format", test_response)
    check("LLM identity and prompt", test_prompt)

    passed = sum(success for _, success in results)
    failed = len(results) - passed

    print("\n" + "=" * 55)
    print(f"Checks: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("IRIS V3.1 STABILITY CHECK: PASS")
    else:
        print("IRIS V3.1 STABILITY CHECK: FAIL")


if __name__ == "__main__":
    main()
