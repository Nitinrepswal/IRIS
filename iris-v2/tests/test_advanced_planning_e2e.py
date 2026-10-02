from models.llm_model import LLMModel
from core.planner import PlanningEngine
from core.multi_step_executor import MultiStepExecutor
from core.tool_layer import ToolLayer


def main():
    model = LLMModel()

    planner = PlanningEngine(model)
    tool_layer = ToolLayer()
    executor = MultiStepExecutor(tool_layer)

    request = "Find my resume."

    print("User:")
    print(request)

    plan = planner.plan(request)

    print("\nGenerated plan:")
    print(plan)

    tasks = plan["tasks"]

    print("\nExecuting plan...")

    results = executor.execute(tasks)

    print("\nExecution results:")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()