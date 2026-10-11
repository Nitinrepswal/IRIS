
import time

from core.vision import VisionEngine
from core.web_knowledge import WebKnowledge
from core.multimodal import MultiModalInput
from models.llm_model import LLMModel


class AdvancedRelease:
    def __init__(self):
        self.model = LLMModel()
        self.vision = VisionEngine()
        self.web = WebKnowledge()
        self.multimodal = MultiModalInput()

    def test_llm(self):
        start = time.perf_counter()

        try:
            response = self.model.generate(
                "Say hello in one short sentence."
            )
            elapsed = time.perf_counter() - start

            return {
                "success": bool(response),
                "time": round(elapsed, 2),
            }
        except Exception as error:
            return {
                "success": False,
                "time": round(time.perf_counter() - start, 2),
                "message": str(error),
            }

    def test_vision(self):
        image_path = "sandbox/screenshots/multimodal_screen.png"
        start = time.perf_counter()

        try:
            result = self.vision.execute(image_path)
            elapsed = time.perf_counter() - start

            success = (
                isinstance(result, dict)
                and result.get("success") is True
            )

            return {
                "success": success,
                "time": round(elapsed, 2),
                "under_90_seconds": elapsed < 90,
                **(
                    {"message": result.get("message", "Vision failed")}
                    if not success and isinstance(result, dict)
                    else {}
                ),
            }

        except Exception as error:
            return {
                "success": False,
                "time": round(time.perf_counter() - start, 2),
                "under_90_seconds": False,
                "message": str(error),
            }

    def test_web(self):
        start = time.perf_counter()

        try:
            result = self.web.execute(
                "What is Python programming language?"
            )
            elapsed = time.perf_counter() - start

            success = (
                isinstance(result, dict)
                and result.get("success") is True
            )

            return {
                "success": success,
                "time": round(elapsed, 2),
                **(
                    {"message": result.get("message", "Web test failed")}
                    if not success and isinstance(result, dict)
                    else {}
                ),
            }

        except Exception as error:
            return {
                "success": False,
                "time": round(time.perf_counter() - start, 2),
                "message": str(error),
            }

    def test_multimodal(self):
        try:
            result = self.multimodal.execute(
                "text",
                "Hello IRIS",
            )

            success = (
                isinstance(result, dict)
                and result.get("type") == "text"
                and result.get("content") == "Hello IRIS"
            )

            return {
                "success": success,
                **(
                    {"message": "Unexpected multimodal result"}
                    if not success
                    else {}
                ),
            }

        except Exception as error:
            return {
                "success": False,
                "message": str(error),
            }

    def run(self):
        tests = {
            "llm": self.test_llm(),
            "vision": self.test_vision(),
            "web": self.test_web(),
            "multimodal": self.test_multimodal(),
        }

        passed = sum(
            1
            for result in tests.values()
            if result["success"]
        )
        total = len(tests)

        performance_ok = tests["vision"].get(
            "under_90_seconds",
            False,
        )

        tests["passed"] = passed
        tests["total"] = total
        tests["performance_ok"] = performance_ok
        tests["release_ready"] = (
            passed == total and performance_ok
        )

        return tests
