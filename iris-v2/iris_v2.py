from core.iris_core import IRISCore
from models.llm_model import LLMModel
from core.permission import PermissionSystem
from core.confirmation import ConfirmationSystem
from core.sandbox import Sandbox
from core.ui import IRISUI
from core.logger import IRISLogger


class IRISV2:
    def __init__(self):
        self.core = IRISCore()
        self.model = LLMModel()

        self.permissions = PermissionSystem()
        self.confirmation = ConfirmationSystem()
        self.sandbox = Sandbox()

        self.ui = IRISUI()
        self.logger = IRISLogger()

        self.core.set_model(self.model)

    def start(self):
        self.ui.show_banner()

        self.logger.log(
            "iris_v2_started"
        )

        self.ui.show_status(
            "IRIS V2 is online."
        )

        while True:
            message = input("\nYou: ")

            if message.lower() == "exit":
                self.logger.log(
                    "iris_v2_shutdown"
                )

                self.ui.show_goodbye()
                break

            response = self.core.process(
                message
            )

            self.logger.log(
                "user_message",
                {
                    "message": message
                }
            )

            self.ui.show_response(
                response
            )


def main():
    iris = IRISV2()
    iris.start()


if __name__ == "__main__":
    main()