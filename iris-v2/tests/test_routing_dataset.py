
import json
import unittest
from pathlib import Path


class TestRoutingDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        project_root = Path(__file__).resolve().parent.parent
        dataset_path = project_root / "data" / "routing_evaluation.json"

        with dataset_path.open("r", encoding="utf-8") as file:
            cls.dataset = json.load(file)

    def test_dataset_is_not_empty(self):
        self.assertGreater(len(self.dataset), 0)

    def test_unique_ids(self):
        ids = [item["id"] for item in self.dataset]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_fields(self):
        required = {
            "id",
            "message",
            "expected_intent",
            "expected_tool"
        }

        for item in self.dataset:
            with self.subTest(item=item.get("id")):
                self.assertTrue(required.issubset(item))

    def test_messages_are_non_empty(self):
        for item in self.dataset:
            with self.subTest(item=item.get("id")):
                self.assertIsInstance(item["message"], str)
                self.assertTrue(item["message"].strip())

    def test_valid_labels(self):
        intents = {
            "chat",
            "information",
            "filesystem",
            "memory",
            "terminal"
        }

        tools = {
            "none",
            "filesystem_search",
            "filesystem_edit",
            "memory",
            "terminal",
            "browser",
            "application",
            "system"
        }

        for item in self.dataset:
            with self.subTest(item=item.get("id")):
                self.assertIn(item["expected_intent"], intents)
                self.assertIn(item["expected_tool"], tools)

    def test_dataset_has_expected_size(self):
        self.assertEqual(len(self.dataset), 20)


if __name__ == "__main__":
    unittest.main()
