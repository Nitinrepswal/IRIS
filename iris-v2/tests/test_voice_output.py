from app.voice_output import VoiceOutput


def main():
    voice = VoiceOutput()

    print("IRIS Voice Output")
    print("Speaking...")

    voice.speak(
        "Hello. I am IRIS. Voice output is working."
    )

    print("Voice output complete.")


if __name__ == "__main__":
    main()