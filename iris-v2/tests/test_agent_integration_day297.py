
from agent.iris_agent import IRISAgent


class FakeModel:
    def structured_chat(self, messages):
        prompt = messages[0]["content"].lower()

        if "advanced planning engine" in prompt:
            return {
                "goal": "Find example files",
                "tasks": [
                    {
                        "step": 1,
                        "action": "search",
                        "target": "example",
                        "tool": "filesystem_search",
                    }
                ],
            }

        if "task decomposition engine" in prompt:
            return {
                "goal": "Find example files",
                "tasks": [
                    {
                        "step": 1,
                        "action": "search",
                        "target": "example",
                    }
                ],
            }

        raise AssertionError("Unexpected model prompt")


class FakeToolLayer:
    def __init__(self):
        self.calls = []

    def execute(self, tool_name, arguments):
        self.calls.append((tool_name, arguments))
        return {
            "success": True,
            "result": ["example.py"],
            "retry": False,
        }


def main():
    tool_layer = FakeToolLayer()
    agent = IRISAgent(FakeModel(), tool_layer)

    result = agent.run("Find example files")

    assert len(tool_layer.calls) == 1
    assert tool_layer.calls[0][0] == "filesystem_search"
    assert tool_layer.calls[0][1]["query"] == "example"

    assert result["goal_state"]["status"] == "completed"
    assert result["evaluation"]["success"] is True
    assert result["results"][0]["result"]["result"] == ["example.py"]

    print("DAY 297 AGENT INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()
