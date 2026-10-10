
import unittest

from core.multi_tool_router import MultiToolRouter


class FakeModel:
    def __init__(self, response):
        self.response = response

    def structured_chat(self, messages):
        return self.response


class TestMultiToolRouter(unittest.TestCase):
    def test_multi_tool_request(self):
        model = FakeModel({
            "steps": [
                {
                    "step": 1,
                    "action": "search",
                    "target": "resume",
                    "tool": "filesystem_search"
                },
                {
                    "step": 2,
                    "action": "read",
                    "target": "step 1 result",
                    "tool": "file_reader"
                }
            ],
            "needs_clarification": False,
            "question": ""
        })

        result = MultiToolRouter(model).route(
            "Find my resume and read it"
        )

        self.assertTrue(result["valid"])
        self.assertEqual(len(result["steps"]), 2)
        self.assertEqual(result["steps"][0]["step"], 1)
        self.assertEqual(result["steps"][1]["tool"], "file_reader")

    def test_single_tool_request(self):
        model = FakeModel({
            "steps": [{
                "step": 1,
                "action": "search",
                "target": "resume",
                "tool": "filesystem_search"
            }],
            "needs_clarification": False,
            "question": ""
        })

        result = MultiToolRouter(model).route("Find my resume")

        self.assertTrue(result["valid"])
        self.assertEqual(len(result["steps"]), 1)

    def test_clarification_request(self):
        model = FakeModel({
            "steps": [],
            "needs_clarification": True,
            "question": "Which file do you mean?"
        })

        result = MultiToolRouter(model).route("Open it")

        self.assertTrue(result["needs_clarification"])
        self.assertEqual(result["steps"], [])

    def test_empty_request(self):
        result = MultiToolRouter(FakeModel({})).route("")

        self.assertFalse(result["valid"])

    def test_unsupported_tool(self):
        model = FakeModel({
            "steps": [{
                "step": 1,
                "action": "do",
                "target": "something",
                "tool": "unknown_tool"
            }],
            "needs_clarification": False,
            "question": ""
        })

        result = MultiToolRouter(model).route("Do something")

        self.assertFalse(result["valid"])

    def test_duplicate_steps(self):
        model = FakeModel({
            "steps": [
                {"step": 1, "action": "search", "target": "a",
                 "tool": "filesystem_search"},
                {"step": 1, "action": "read", "target": "b",
                 "tool": "file_reader"}
            ],
            "needs_clarification": False,
            "question": ""
        })

        result = MultiToolRouter(model).route("Search and read")

        self.assertFalse(result["valid"])

    def test_invalid_model_response(self):
        result = MultiToolRouter(FakeModel("not JSON")).route("Find a file")

        self.assertFalse(result["valid"])

    def test_nonconsecutive_steps(self):
        model = FakeModel({
            "steps": [{
                "step": 2,
                "action": "search",
                "target": "resume",
                "tool": "filesystem_search"
            }],
            "needs_clarification": False,
            "question": ""
        })

        result = MultiToolRouter(model).route("Find my resume")

        self.assertFalse(result["valid"])


if __name__ == "__main__":
    unittest.main()
