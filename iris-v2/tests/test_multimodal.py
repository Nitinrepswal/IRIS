from core.multimodal import MultiModalInput


def main():
    multimodal = MultiModalInput()

    text_result = multimodal.execute(
        "text",
        "Hello IRIS"
    )

    print("Text:")
    print(text_result)

    voice_result = multimodal.execute(
        "voice",
        "Open calculator"
    )

    print("\nVoice:")
    print(voice_result)

    screenshot_result = multimodal.execute(
        "screenshot"
    )

    print("\nScreenshot:")
    print(screenshot_result)


if __name__ == "__main__":
    main()