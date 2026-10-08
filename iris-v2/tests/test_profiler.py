import time

from core.profiler import PerformanceProfiler


def fast_operation():
    time.sleep(0.05)

    return "fast"


def slow_operation():
    time.sleep(0.15)

    return "slow"


def failing_operation():
    raise ValueError("Test failure")


def main():
    print("IRIS V3.1 PERFORMANCE PROFILER TEST")
    print("=" * 50)

    profiler = PerformanceProfiler()

    fast_result = profiler.measure(
        "fast_operation",
        fast_operation
    )

    slow_result = profiler.measure(
        "slow_operation",
        slow_operation
    )

    print("\nResults:")
    print("Fast:", fast_result)
    print("Slow:", slow_result)

    try:
        profiler.measure(
            "failing_operation",
            failing_operation
        )
    except ValueError:
        print("Failure captured: True")

    print("\nRecords:")

    for record in profiler.get_records():
        print(record)

    print("\nAverages:")

    print(
        "fast_operation:",
        profiler.get_average("fast_operation")
    )

    print(
        "slow_operation:",
        profiler.get_average("slow_operation")
    )

    slowest = profiler.get_slowest()

    print("\nSlowest operation:")
    print(slowest)

    passed = (
        fast_result == "fast"
        and slow_result == "slow"
        and len(profiler.get_records()) == 3
        and profiler.get_average("fast_operation") > 0
        and profiler.get_average("slow_operation") > 0
        and slowest["name"] == "slow_operation"
    )

    profiler.clear()

    print("\n" + "=" * 50)

    if passed:
        print("PERFORMANCE PROFILER TEST: PASS")
    else:
        print("PERFORMANCE PROFILER TEST: FAIL")


if __name__ == "__main__":
    main()