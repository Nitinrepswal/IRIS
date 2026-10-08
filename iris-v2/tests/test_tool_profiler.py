import time

from core.tool_profiler import ToolProfiler


class FastTool:
    name = "fast_tool"

    def execute(self, **arguments):
        time.sleep(0.05)

        return {
            "success": True,
            "message": "Fast tool completed."
        }


class SlowTool:
    name = "slow_tool"

    def execute(self, **arguments):
        time.sleep(0.15)

        return {
            "success": True,
            "message": "Slow tool completed."
        }


class FailingTool:
    name = "failing_tool"

    def execute(self, **arguments):
        raise RuntimeError("Tool failure")


def main():
    print("IRIS V3.1 TOOL EXECUTION PROFILER TEST")
    print("=" * 55)

    profiler = ToolProfiler()

    fast_result = profiler.execute(
        FastTool()
    )

    slow_result = profiler.execute(
        SlowTool()
    )

    print("\nResults:")
    print("Fast:", fast_result)
    print("Slow:", slow_result)

    try:
        profiler.execute(
            FailingTool()
        )

    except RuntimeError:
        print("Failure captured: True")

    print("\nRecords:")

    for record in profiler.get_records():
        print(record)

    print("\nAverages:")

    print(
        "fast_tool:",
        profiler.get_average("fast_tool")
    )

    print(
        "slow_tool:",
        profiler.get_average("slow_tool")
    )

    slowest = profiler.get_slowest()

    print("\nSlowest tool:")
    print(slowest)

    passed = (
        fast_result["success"]
        and slow_result["success"]
        and len(profiler.get_records()) == 3
        and profiler.get_average("fast_tool") > 0
        and profiler.get_average("slow_tool") > 0
        and slowest["tool"] == "slow_tool"
    )

    profiler.clear()

    print("\n" + "=" * 55)

    if passed:
        print("TOOL EXECUTION PROFILER TEST: PASS")
    else:
        print("TOOL EXECUTION PROFILER TEST: FAIL")


if __name__ == "__main__":
    main()