from tools.application import ApplicationTool


def main():
    tool = ApplicationTool()

    print("Tool:", tool.name)
    print("Description:", tool.description)

    result = tool.execute(
        "Calculator"
    )

    print("\nAllowed application:")
    print(result)

    result = tool.execute(
        "UnknownApplication"
    )

    print("\nBlocked application:")
    print(result)


if __name__ == "__main__":
    main()