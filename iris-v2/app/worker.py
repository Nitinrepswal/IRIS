from PySide6.QtCore import QObject, Signal, Slot

from core.iris_core import IRISCore
from models.llm_model import LLMModel
from app.voice import VoiceInput
from app.voice_output import VoiceOutput


class IRISWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.model = LLMModel()
        self.core = IRISCore()
        self.core.set_model(self.model)

    @Slot(str)
    def process(self, message):
        try:
            response = self.core.process(message)
            self.finished.emit(response)
        except Exception as error:
            self.error.emit(str(error))


class VoiceWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.voice = VoiceInput()
        self.running = True

    @Slot()
    def listen(self):
        if not self.running:
            return

        try:
            text = self.voice.listen()
            if self.running:
                self.finished.emit(text)
        except Exception as error:
            if self.running:
                self.error.emit(str(error))

    @Slot()
    def stop(self):
        self.running = False


class SpeechWorker(QObject):
    finished = Signal()
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.voice = VoiceOutput()
        self.running = True

    @Slot(str)
    def speak(self, text):
        if not self.running:
            return

        try:
            self.voice.speak(text)

            if self.running:
                self.finished.emit()

        except Exception as error:
            if self.running:
                self.error.emit(str(error))

    @Slot()
    def stop(self):
        self.running = False