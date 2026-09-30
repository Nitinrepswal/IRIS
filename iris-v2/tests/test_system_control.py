from core.system_control import SystemControl


def main():
    controller = SystemControl()

    commands = [
        "system information",
        "system info",
        "about my computer"
    ]

    for command in commands:
        print("Command:", command)

        result = controller.execute(
            command
        )

        print(result)
        print()


if __name__ == "__main__":
    main()