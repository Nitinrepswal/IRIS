from app.voice import VoiceInput


def main():
    voice = VoiceInput()

    print("IRIS Voice Input")
    print("Speak now. Stop talking when finished.")

    text = voice.listen()

    if text:
        print("You said:", text)
    else:
        print("No speech detected.")


if __name__ == "__main__":
    main()