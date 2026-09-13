from tools.terminal import TerminalTool


def main():
    tool = TerminalTool()

    print("Tool:", tool.name)
    print("Description:", tool.description)

    result = tool.execute("echo Hello from IRIS.")

    print("\nReturn code:", result["return_code"])
    print("Output:", result["stdout"])

    blocked = tool.execute("rm test_file.txt")

    print("Blocked command:", blocked)


if __name__ == "__main__":
    main()