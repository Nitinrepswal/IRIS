from tools.system import SystemTool


def main():
    tool = SystemTool()

    print("Tool:", tool.name)
    print("Description:", tool.description)

    result = tool.execute()

    print("\nSystem information:")

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()