from core.computer_control import ComputerControl


def main():
    computer = ComputerControl()

    print("Computer Control V1")

    print("\nSystem information:")

    system = computer.system_information()

    for key, value in system.items():
        print(f"{key}: {value}")

    print("\nWebpage:")

    webpage = computer.open_webpage(
        "https://example.com"
    )

    print("URL:", webpage["url"])
    print("Status:", webpage["status"])
    print("Content:", webpage["text"])

    print("\nApplication:")

    application = computer.launch_application(
        "Calculator"
    )

    print(application)


if __name__ == "__main__":
    main()