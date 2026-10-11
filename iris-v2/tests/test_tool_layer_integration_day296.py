
from core.tool_layer import ToolLayer


def main():
    layer = ToolLayer()

    expected_tools = {
        "filesystem_search",
        "file_editor",
        "file_reader",
        "terminal",
    }

    assert set(layer.tool_names()) == expected_tools

    search_result = layer.execute(
        "filesystem_search",
        {
            "directory": "tests",
            "query": "iris_core",
        },
    )

    assert search_result["success"] is True
    assert any(
        "test_iris_core" in path
        for path in search_result["result"]
    )

    read_result = layer.execute(
        "file_reader",
        {
            "path": "tests/test_iris_core_validation_day296.py",
        },
    )

    assert read_result["success"] is True
    assert "IRISCore" in read_result["result"]

    invalid_result = layer.execute(
        "nonexistent_tool",
        {},
    )

    assert invalid_result["success"] is False
    assert invalid_result["error"] == "tool_not_found"

    print("DAY 296 TOOL LAYER INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()
