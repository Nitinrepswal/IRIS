import time

import numpy as np
import sounddevice as sd
import speech_recognition as sr


class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(
        self,
        sample_rate=16000,
        block_duration=0.1,
        silence_duration=1.0,
        max_duration=8
    ):
        print("Listening...")

        blocks = []

        block_size = int(
            sample_rate * block_duration
        )

        silence_blocks = int(
            silence_duration / block_duration
        )

        start_time = time.time()

        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        ) as stream:

            calibration_blocks = []

            for _ in range(10):
                data, _ = stream.read(block_size)
                calibration_blocks.append(data.copy())

            calibration = np.concatenate(
                calibration_blocks,
                axis=0
            )

            noise_level = np.abs(
                calibration.astype(np.float32)
            ).mean()

            threshold = max(
                noise_level * 2.5,
                300
            )

            started = False
            silent_count = 0

            while (
                time.time() - start_time
                < max_duration
            ):
                data, _ = stream.read(block_size)

                block = data.copy()

                volume = np.abs(
                    block.astype(np.float32)
                ).mean()

                if volume > threshold:
                    started = True
                    silent_count = 0

                elif started:
                    silent_count += 1

                    if silent_count >= silence_blocks:
                        break

                if started:
                    blocks.append(block)

        if not started or not blocks:
            print("No speech detected.")
            return ""

        audio = np.concatenate(
            blocks,
            axis=0
        )

        audio_data = sr.AudioData(
            audio.tobytes(),
            sample_rate,
            2
        )

        print("Processing speech...")

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