import subprocess


class VoiceOutput:
    def __init__(self, rate=180):
        self.rate = rate

    def speak(self, text):
        if not text:
            return

        subprocess.run(
            [
                "say",
                "-r",
                str(self.rate),
                text
            ],
            check=True
        )