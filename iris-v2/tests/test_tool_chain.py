
from core.tool_chain import ToolChainPlanner


def main():
    print("IRIS DAY 224 TOOL CHAIN PLANNING TEST")
    print("=" * 50)

    planner = ToolChainPlanner()
    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "user's resume",
            "tool": "filesystem_search"
        },
        {
            "step": 2,
            "action": "read",
            "target": "resume found in step 1",
            "tool": "file_reader"
        },
        {
            "step": 3,
            "action": "summarize",
            "target": "resume content from step 2",
            "tool": "llm"
        }
    ]

    dependencies = [
        {"step": 1, "depends_on": []},
        {"step": 2, "depends_on": [1]},
        {"step": 3, "depends_on": [2]}
    ]

    result = planner.build(tasks, dependencies)

    check("Valid chain accepted", result["valid"])
    check("Three tasks included", len(result["chain"]) == 3)
    check(
        "Search comes before read",
        result["chain"][0]["tool"] == "filesystem_search"
        and result["chain"][1]["tool"] == "file_reader"
    )
    check(
        "Read dependency preserved",
        result["chain"][1]["depends_on"] == [1]
    )
    check(
        "Summary depends on read",
        result["chain"][2]["depends_on"] == [2]
    )

    cycle_dependencies = [
        {"step": 1, "depends_on": [2]},
        {"step": 2, "depends_on": [1]},
        {"step": 3, "depends_on": [2]}
    ]

    result = planner.build(tasks, cycle_dependencies)

    check("Dependency cycle rejected", result["valid"] is False)

    invalid_dependencies = [
        {"step": 1, "depends_on": []},
        {"step": 2, "depends_on": [99]},
        {"step": 3, "depends_on": [2]}
    ]

    result = planner.build(tasks, invalid_dependencies)

    check("Unknown dependency rejected", result["valid"] is False)

    invalid_tasks = [
        {
            "step": 1,
            "action": "run",
            "target": "some command",
            "tool": "unknown_tool"
        }
    ]

    result = planner.build(
        invalid_tasks,
        [{"step": 1, "depends_on": []}]
    )

    check("Unknown tool rejected", result["valid"] is False)

    result = planner.build("invalid", [])

    check("Invalid input rejected", result["valid"] is False)

    print("\n" + "=" * 50)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("TOOL CHAIN PLANNING: PASS")
    else:
        print("TOOL CHAIN PLANNING: FAIL")


if __name__ == "__main__":
    main()
