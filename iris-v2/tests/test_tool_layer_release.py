from core.tool_layer import ToolLayer


def main():
    layer = ToolLayer()

    print("Tool names:")
    for name in layer.tool_names():
        print("-", name)

    print("\nTool status:")
    for name, info in layer.tool_status().items():
        print(f"{name}: {info}")


if __name__ == "__main__":
    main()