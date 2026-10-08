from core.logger import Logger


def main():
    print("IRIS V3.1 LOGGING V2 TEST")
    print("=" * 50)

    path = "sandbox/day203_logs.json"

    logger = Logger(path)

    logger.clear()

    logger.debug(
        "Debug message",
        context="Day 203"
    )

    logger.info(
        "IRIS started",
        context="startup"
    )

    logger.warning(
        "Test warning",
        context="test"
    )

    logger.error(
        "Test error",
        context="test"
    )

    logs = logger.get_logs()

    print("\nLog entries:")

    for entry in logs:
        print(entry)

    print("\nLog levels:")

    for level in [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR"
    ]:
        count = len(
            logger.get_by_level(level)
        )

        print(f"{level}: {count}")

    passed = (
        len(logs) == 4
        and all(
            "timestamp" in entry
            and "level" in entry
            and "message" in entry
            for entry in logs
        )
    )

    logger.clear()

    print("\n" + "=" * 50)

    if passed:
        print("LOGGING V2 TEST: PASS")
    else:
        print("LOGGING V2 TEST: FAIL")


if __name__ == "__main__":
    main()