from core.confirmation import ConfirmationSystem


def main():
    confirmation = ConfirmationSystem()

    print("IRIS Human Confirmation System")

    print("\nBrowser:")
    print(
        "Requires confirmation:",
        confirmation.requires_confirmation("browser")
    )

    print("\nTerminal:")
    print(
        "Requires confirmation:",
        confirmation.requires_confirmation("terminal")
    )

    print("\nUnknown action:")
    print(
        "Blocked:",
        confirmation.is_blocked("unknown")
    )

    print("\nSafe action:")
    print(
        "Confirmed:",
        confirmation.confirm("browser")
    )

    print("\nRisky action:")
    confirmation.confirm("terminal")


if __name__ == "__main__":
    main()