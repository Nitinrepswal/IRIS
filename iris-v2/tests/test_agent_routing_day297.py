
from core.planner import PlanningEngine
from core.task_decomposer import TaskDecomposer


class FakeModel:
    def structured_chat(self, messages):
        prompt = messages[0]["content"]

        if "advanced planning engine" in prompt.lower():
            return {
                "goal": "Find test files",
                "tasks": [
                    {
                        "step": 1,
                        "action": "search",
                        "target": "files containing test",
                        "tool": "filesystem_search",
                    }
                ],
            }

        if "task decomposition engine" in prompt.lower():
            return {
                "goal": "Find test files",
                "tasks": [
                    {
                        "step": 1,
                        "action": "search",
                        "target": "files containing test",
                    }
                ],
            }

        raise AssertionError("Unexpected model prompt")


def main():
    model = FakeModel()

    plan = PlanningEngine(model).plan("Find test files")
    decomposition = TaskDecomposer(model).decompose("Find test files")

    assert plan["tasks"][0]["tool"] == "filesystem_search"
    assert "tool" not in decomposition["tasks"][0]

    print("DAY 297 AGENT ROUTING DIAGNOSIS: PASS")


if __name__ == "__main__":
    main()
