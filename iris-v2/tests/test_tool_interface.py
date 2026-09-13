from tools.test_tool import EchoTool


def main():
    tool = EchoTool()

    print("Tool name:", tool.name)
    print("Tool description:", tool.description)

    result = tool.execute(message="Hello from IRIS.")

    print("Tool result:", result)


if __name__ == "__main__":
    main()