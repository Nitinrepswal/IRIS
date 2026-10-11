
from core.autonomous_task import AutonomousTaskEngine
from core.tool_layer import ToolLayer


def main():
    engine = AutonomousTaskEngine(
        tool_layer=ToolLayer(),
        max_retries=0,
    )

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "test_iris_core_validation_day296.py",
            "tool": "filesystem_search",
        },
        {
            "step": 2,
            "action": "read",
            "target": "tests/test_iris_core_validation_day296.py",
            "tool": "file_reader",
        },
    ]

    result = engine.execute(
        "Find and read the Day 296 validation test",
        tasks,
    )

    assert result["status"] == "completed", result
    assert result["total_steps"] == 2
    assert result["current_step"] == 2
    assert len(result["results"]) == 2

    first = result["results"][0]
    assert first["success"] is True
    assert first["observation"]["status"] == "success"

    second = result["results"][1]
    assert second["success"] is True
    assert "IRISCore" in second["result"]["result"]
    assert second["observation"]["status"] == "success"

    print("DAY 297 AUTONOMOUS TASK TEST: PASS")


if __name__ == "__main__":
    main()
