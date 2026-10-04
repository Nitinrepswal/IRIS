import subprocess


class VoiceOutput:
    def __init__(self, rate=190):
        self.rate = rate
        self.process = None

    def speak(self, text):
        if not text:
            return

        self.stop()

        self.process = subprocess.Popen(
            [
                "say",
                "-r",
                str(self.rate),
                text
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def stop(self):
        if self.process is None:
            return

        if self.process.poll() is None:
            self.process.terminate()

        self.process = None