import time

from PySide6.QtCore import QObject, Signal, Slot

from core.iris_core import IRISCore
from core.tool_manager import ToolManager
from core.permission_control import PermissionControl
from models.llm_model import LLMModel
from memory.memory_system import MemorySystem
from app.voice import VoiceInput
from app.voice_output import VoiceOutput


class IRISWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    permission_required = Signal(str, str)

    def __init__(self):
        super().__init__()

        self.model = LLMModel()

        self.core = IRISCore()
        self.core.set_model(self.model)

        self.memory = MemorySystem()
        self.core.set_memory(self.memory)

        self.tool_manager = ToolManager()
        self.permission_control = PermissionControl()

    def detect_action(self, message):
        text = message.lower().strip()

        if self.tool_manager.app_control.detect_application(message):
            return "application"

        if (
            text.startswith("find file ")
            or text.startswith("read file ")
            or text.startswith("create file ")
        ):
            return "filesystem"

        return None

    @Slot(str)
    def process(self, message):
        try:
            action = self.detect_action(message)

            if action is not None:
                if not self.permission_control.is_allowed(action):
                    self.finished.emit(
                        f"Permission denied for {action}."
                    )
                    return

                if self.permission_control.requires_confirmation(action):
                    self.permission_required.emit(
                        action,
                        message
                    )
                    return

            self.execute_message(message)

        except Exception as error:
            self.error.emit(str(error))

    @Slot(str)
    def execute_message(self, message):
        try:
            start = time.perf_counter()

            tool_response = self.tool_manager.execute(message)

            if tool_response is not None:
                elapsed = time.perf_counter() - start

                print(
                    f"[IRIS] Tool response: "
                    f"{elapsed:.2f}s"
                )

                self.finished.emit(tool_response)
                return

            response_start = time.perf_counter()

            response = self.core.process(message)

            response_time = (
                time.perf_counter()
                - response_start
            )

            total_time = (
                time.perf_counter()
                - start
            )

            print(
                f"[IRIS] LLM: "
                f"{response_time:.2f}s | "
                f"Total: "
                f"{total_time:.2f}s"
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
        try:
            self.running = True

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
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.voice = VoiceOutput()

    @Slot(str)
    def speak(self, text):
        try:
            self.voice.speak(text)

        except Exception as error:
            self.error.emit(str(error))

    @Slot()
    def stop(self):
        self.voice.stop()