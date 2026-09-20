from PySide6.QtCore import QObject, Signal, Slot

from core.iris_core import IRISCore
from models.llm_model import LLMModel


class IRISWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()

        self.model = LLMModel()
        self.core = IRISCore()

        self.core.set_model(
            self.model
        )

    @Slot(str)
    def process(self, message):
        try:
            response = self.core.process(
                message
            )

            self.finished.emit(
                response
            )

        except Exception as error:
            self.error.emit(
                str(error)
            )