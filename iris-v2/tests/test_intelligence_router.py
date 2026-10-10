
import unittest

from core.intelligence_router import IntelligenceRouter


class FakeModel:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def structured_chat(self, messages):
        if self.calls >= len(self.responses):
            raise AssertionError("Unexpected model call.")

        response = self.responses[self.calls]
        self.calls += 1
        return response


class TestIntelligenceRouter(unittest.TestCase):
    def test_empty_request(self):
        router = IntelligenceRouter(FakeModel([]))
        result = router.route("")

        self.assertFalse(result["valid"])
        self.assertFalse(result["executed"])
        self.assertEqual(result["steps"], [])

    def test_vague_request_needs_clarification(self):
        router = IntelligenceRouter(FakeModel([]))
        result = router.route("Do it")

        self.assertTrue(result["needs_clarification"])
        self.assertEqual(result["steps"], [])
        self.assertFalse(result["executed"])

    def test_multi_step_plan(self):
        model = FakeModel([
            {
                "intent": "filesystem",
                "reason": "Find and read a file.",
                "confidence": 0.95,
            },
            {
                "steps": [
                    {
                        "step": 1,
                        "action": "search",
                        "target": "resume",
                        "tool": "filesystem_search",
                    },
                    {
                        "step": 2,
                        "action": "read",
                        "target": "step 1 result",
                        "tool": "file_reader",
                    },
                ],
                "needs_clarification": False,
                "question": "",
            },
        ])

        result = IntelligenceRouter(model).route(
            "Find my resume and read it"
        )

        self.assertTrue(result["valid"], result["reason"])
        self.assertEqual(len(result["steps"]), 2)
        self.assertEqual(
            result["steps"][1]["depends_on"],
            [1],
        )
        self.assertFalse(result["executed"])

    def test_multi_tool_clarification(self):
        model = FakeModel([
            {
                "intent": "filesystem",
                "reason": "File request.",
                "confidence": 0.95,
            },
            {
                "steps": [],
                "needs_clarification": True,
                "question": "Which file do you mean?",
            },
        ])

        result = IntelligenceRouter(model).route(
            "Find my resume and read it"
        )

        self.assertTrue(
            result["needs_clarification"],
            result["reason"],
        )
        self.assertEqual(
            result["question"],
            "Which file do you mean?",
        )
        self.assertEqual(result["steps"], [])
        self.assertFalse(result["executed"])


if __name__ == "__main__":
    unittest.main()
