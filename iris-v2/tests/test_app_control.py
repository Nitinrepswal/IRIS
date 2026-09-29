from core.app_control import AppControl


def main():
    controller = AppControl()

    commands = [
        "open calculator",
        "launch TextEdit",
        "start Safari"
    ]

    for command in commands:
        print("Command:", command)

        application = controller.detect_application(
            command
        )

        print("Detected:", application)

        if application:
            result = controller.execute(
                command
            )
            print("Result:", result)

        print()


if __name__ == "__main__":
    main()