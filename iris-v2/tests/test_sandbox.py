from core.sandbox import Sandbox


def main():
    sandbox = Sandbox()

    print("IRIS Sandbox Security")

    print("\nSafe path:")

    safe_path = sandbox.get_safe_path(
        "notes.txt"
    )

    print(safe_path)

    print("\nNested safe path:")

    nested_path = sandbox.get_safe_path(
        "data/test.txt"
    )

    print(nested_path)

    print("\nUnsafe path:")

    try:
        sandbox.get_safe_path(
            "../secret.txt"
        )

        print("ERROR: unsafe path was allowed")

    except PermissionError as error:
        print("Blocked:", error)

    print("\nAbsolute unsafe path:")

    try:
        sandbox.get_safe_path(
            "/tmp/test.txt"
        )

        print("ERROR: unsafe path was allowed")

    except PermissionError as error:
        print("Blocked:", error)


if __name__ == "__main__":
    main()