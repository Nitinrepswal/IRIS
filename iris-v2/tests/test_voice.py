from app.voice import VoiceInput


def main():
    voice = VoiceInput()

    print("IRIS Voice Input")
    print("Speak for 5 seconds...")

    text = voice.listen(
        seconds=5
    )

    if text:
        print("You said:", text)
    else:
        print("No speech detected.")


if __name__ == "__main__":
    main()