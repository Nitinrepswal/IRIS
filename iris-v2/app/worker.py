from PySide6.QtCore import QObject, Signal, Slot

from core.iris_core import IRISCore
from core.app_control import AppControl
from core.file_control import FileControl
from core.web_control import WebControl
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

        self.app_control = AppControl()
        self.file_control = FileControl()
        self.web_control = WebControl()

    @Slot(str)
    def process(self, message):
        try:
            app_response = self.app_control.execute(
                message
            )

            if app_response is not None:
                self.finished.emit(app_response)
                return

            file_response = self.file_control.execute(
                message
            )

            if file_response is not None:
                self.finished.emit(file_response)
                return

            web_response = self.web_control.execute(
                message
            )

            if web_response is not None:
                self.finished.emit(web_response)
                return

            response = self.core.process(
                message
            )

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