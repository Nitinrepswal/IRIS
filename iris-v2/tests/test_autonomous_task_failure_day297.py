
from core.autonomous_task import AutonomousTaskEngine


class FakeToolLayer:
    def __init__(self):
        self.calls = []

    def execute(self, tool_name, arguments):
        self.calls.append((tool_name, arguments))
        return {
            "success": False,
            "error": "tool_not_found",
            "message": "Tool not found.",
            "retry": False,
        }


def main():
    tool_layer = FakeToolLayer()
    engine = AutonomousTaskEngine(tool_layer, max_retries=2)

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "missing_file",
            "tool": "missing_tool",
        },
        {
            "step": 2,
            "action": "read",
            "target": "some_file.txt",
            "tool": "file_reader",
        },
    ]

    result = engine.execute("Test safe failure handling", tasks)

    assert result["status"] == "failed", result
    assert len(result["results"]) == 1
    assert result["results"][0]["success"] is False
    assert len(tool_layer.calls) == 1

    print("DAY 297 AUTONOMOUS FAILURE TEST: PASS")


if __name__ == "__main__":
    main()
