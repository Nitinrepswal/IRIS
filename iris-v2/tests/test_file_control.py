import os

from core.file_control import FileControl


def main():
    controller = FileControl()

    test_directory = "sandbox"
    test_file = os.path.join(
        test_directory,
        "iris_test.txt"
    )

    os.makedirs(
        test_directory,
        exist_ok=True
    )

    print("Creating file...")

    result = controller.write(
        test_file,
        "Hello from IRIS Day 162."
    )

    print(result)

    print()
    print("Reading file...")

    content = controller.read(
        test_file
    )

    print(content)

    print()
    print("Searching for file...")

    matches = controller.search(
        test_directory,
        "iris_test"
    )

    print(matches)


if __name__ == "__main__":
    main()