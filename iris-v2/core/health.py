import time

from models.llm_model import LLMModel
from core.vision import VisionEngine
from core.multimodal import MultiModalInput
from core.web_knowledge import WebKnowledge


class IRISHealth:
    def __init__(self):
        self.model = LLMModel()
        self.vision = VisionEngine()
        self.multimodal = MultiModalInput()
        self.web = WebKnowledge()

    def check_llm(self):
        start = time.perf_counter()

        try:
            result = self.model.generate(
                "Reply with OK."
            )

            elapsed = time.perf_counter() - start

            return {
                "status": "healthy",
                "response": result,
                "time": round(elapsed, 2)
            }

        except Exception as error:
            return {
                "status": "error",
                "message": str(error)
            }

    def check_vision(self):
        image_path = "sandbox/screenshots/multimodal_screen.png"

        start = time.perf_counter()

        try:
            result = self.vision.execute(
                image_path
            )

            elapsed = time.perf_counter() - start

            if not result["success"]:
                return {
                    "status": "error",
                    "message": result["message"]
                }

            return {
                "status": "healthy",
                "time": round(elapsed, 2),
                "under_10_seconds": elapsed < 10
            }

        except Exception as error:
            return {
                "status": "error",
                "message": str(error)
            }

    def check_multimodal(self):
        try:
            result = self.multimodal.execute(
                "text",
                "health check"
            )

            if result.get("success", True) is False:
                return {
                    "status": "error"
                }

            return {
                "status": "healthy"
            }

        except Exception as error:
            return {
                "status": "error",
                "message": str(error)
            }

    def check_web(self):
        start = time.perf_counter()

        try:
            result = self.web.execute(
                "What is Python?"
            )

            elapsed = time.perf_counter() - start

            return {
                "status": (
                    "healthy"
                    if result["success"]
                    else "error"
                ),
                "time": round(elapsed, 2)
            }

        except Exception as error:
            return {
                "status": "error",
                "message": str(error)
            }

    def check_all(self):
        checks = {
            "llm": self.check_llm(),
            "vision": self.check_vision(),
            "multimodal": self.check_multimodal(),
            "web": self.check_web()
        }

        healthy = all(
            result["status"] == "healthy"
            for result in checks.values()
        )

        return {
            "status": "healthy" if healthy else "degraded",
            "components": checks
        }