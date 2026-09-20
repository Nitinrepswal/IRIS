import numpy as np
import sounddevice as sd
import speech_recognition as sr


class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self, seconds=5):
        sample_rate = 16000

        audio = sd.rec(
            int(seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        audio_bytes = audio.tobytes()

        audio_data = sr.AudioData(
            audio_bytes,
            sample_rate,
            2
        )

        try:
            text = self.recognizer.recognize_google(
                audio_data
            )

            return text

        except sr.UnknownValueError:
            return ""

        except sr.RequestError as error:
            raise RuntimeError(
                f"Speech recognition error: {error}"
            )