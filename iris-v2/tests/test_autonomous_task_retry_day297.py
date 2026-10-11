
from core.autonomous_task import AutonomousTaskEngine


class FakeToolLayer:
    def __init__(self):
        self.calls = 0

    def execute(self, tool_name, arguments):
        self.calls += 1

        if self.calls == 1:
            return {
                "success": False,
                "error": "connection_error",
                "message": "Temporary connection failure.",
                "retry": True,
            }

        return {
            "success": True,
            "result": ["tests/example.py"],
            "retry": False,
        }


def main():
    tool_layer = FakeToolLayer()
    engine = AutonomousTaskEngine(
        tool_layer,
        max_retries=1,
    )

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "example",
            "tool": "filesystem_search",
        }
    ]

    result = engine.execute("Test recovery", tasks)

    assert result["status"] == "completed", result
    assert tool_layer.calls == 2
    assert result["results"][0]["attempts"] == 2
    assert result["results"][0]["success"] is True

    print("DAY 297 AUTONOMOUS RETRY TEST: PASS")


if __name__ == "__main__":
    main()
