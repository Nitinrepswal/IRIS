from core.logger import IRISLogger
from core.ui import IRISUI


def main():
    ui = IRISUI()
    logger = IRISLogger()

    ui.show_banner()

    logger.log(
        "system_start",
        {
            "component": "IRIS V2"
        }
    )

    ui.show_status(
        "System started."
    )

    ui.show_response(
        "Computer control is ready."
    )

    logger.log(
        "assistant_response",
        {
            "message": "Computer control is ready."
        }
    )

    ui.show_status(
        "Activity logged."
    )

    print("\nLog entries:")

    logs = logger.get_logs()

    for entry in logs:
        print(
            entry["event"],
            "|",
            entry["details"]
        )

    ui.show_goodbye()


if __name__ == "__main__":
    main()