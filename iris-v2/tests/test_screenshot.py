from core.screenshot import ScreenshotTool


def main():
    tool = ScreenshotTool()

    result = tool.execute("iris_screen.png")

    print("Screenshot result:")
    print(result)


if __name__ == "__main__":
    main()