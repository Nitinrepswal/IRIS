
from core.error_handler import ErrorHandler
from core.logger import Logger
from core.profiler import PerformanceProfiler
from core.tool_profiler import ToolProfiler
from core.response import IRISResponse
from core.conversation_state import ConversationState
from core.context_manager import ContextManager
from models.llm_model import LLMModel


def main():
    print("IRIS V3.1 AUTOMATED REGRESSION TESTS")
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

    def test_error_handler():
        handler = ErrorHandler()
        result = handler.handle(ValueError("test"))
        assert result["success"] is False
        assert result["error_type"] == "ValueError"
        assert len(handler.get_errors()) == 1

    def test_logger():
        logger = Logger("logs/regression_test.json")
        logger.clear()
        logger.info("regression test")
        entries = logger.get_logs()
        assert len(entries) == 1
        assert entries[0]["level"] == "INFO"
        logger.clear()

    def test_profiler():
        profiler = PerformanceProfiler()
        result = profiler.measure("sum", sum, [1, 2, 3])
        assert result == 6
        assert len(profiler.get_records()) == 1
        assert profiler.get_records()[0]["success"] is True

    def test_tool_profiler():
        class SampleTool:
            name = "sample"

            def execute(self, **arguments):
                return {"success": True, "result": "ok"}

        profiler = ToolProfiler()
        result = profiler.execute(SampleTool())
        assert result["success"] is True
        assert profiler.get_records()[0]["tool"] == "sample"

    def test_response():
        response = IRISResponse.success_response(
            "Hello",
            source="llm"
        ).to_dict()

        assert response["success"] is True
        assert response["content"] == "Hello"
        assert response["source"] == "llm"

    def test_conversation_state():
        state = ConversationState()
        state.add_user_message("Hello")
        state.add_assistant_message("Hi")

        assert state.get_turn_count() == 1
        assert len(state.get_messages()) == 2
        assert state.get_context()["last_response"] == "Hi"

    def test_context_manager():
        manager = ContextManager(
            max_messages=2,
            max_characters=100
        )

        messages = [
            {"role": "user", "content": "First"},
            {"role": "assistant", "content": "Second"},
            {"role": "user", "content": "Third"}
        ]

        result = manager.trim_messages(messages)

        assert len(result) == 2
        assert result[-1]["content"] == "Third"

    def test_prompt_structure():
        model = LLMModel()
        prompt = model.system_prompt

        assert "You are IRIS" in prompt
        assert "IDENTITY:" in prompt
        assert "CAPABILITIES:" in prompt
        assert "BEHAVIOR:" in prompt

    check("Error handling", test_error_handler)
    check("Logging", test_logger)
    check("Performance profiler", test_profiler)
    check("Tool profiler", test_tool_profiler)
    check("Unified response", test_response)
    check("Conversation state", test_conversation_state)
    check("Context management", test_context_manager)
    check("Prompt structure", test_prompt_structure)

    passed = sum(success for _, success in results)
    failed = len(results) - passed

    print("\n" + "=" * 55)
    print(f"Total tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("REGRESSION TESTS: PASS")
    else:
        print("REGRESSION TESTS: FAIL")


if __name__ == "__main__":
    main()
