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

        response = self.model.generate(
            "Say hello in one short sentence."
        )

        elapsed = time.perf_counter() - start

        return {
            "success": bool(response),
            "time": round(elapsed, 2)
        }

    def test_vision(self):
        image_path = "sandbox/screenshots/multimodal_screen.png"

        start = time.perf_counter()

        result = self.vision.execute(
            image_path
        )

        elapsed = time.perf_counter() - start

        return {
            "success": result["success"],
            "time": round(elapsed, 2)
        }

    def test_web(self):
        start = time.perf_counter()

        result = self.web.execute(
            "What is Python programming language?"
        )

        elapsed = time.perf_counter() - start

        return {
            "success": result["success"],
            "time": round(elapsed, 2)
        }

    def test_multimodal(self):
        result = self.multimodal.execute(
            "text",
            "Hello IRIS"
        )

        return {
            "success": (
                result.get("type") == "text"
                and result.get("content") == "Hello IRIS"
            )
        }

    def run(self):
        tests = {
            "llm": self.test_llm(),
            "vision": self.test_vision(),
            "web": self.test_web(),
            "multimodal": self.test_multimodal()
        }

        passed = sum(
            1
            for result in tests.values()
            if result["success"]
        )

        total = len(tests)

        tests["passed"] = passed
        tests["total"] = total
        tests["release_ready"] = passed == total

        return tests