from models.llm_model import LLMModel
from core.planner import PlanningEngine


def main():
    model = LLMModel()
    planner = PlanningEngine(model)

    requests = [
        "Find my resume and read it.",
        "Find my resume, read it, and summarize it.",
        "Search the web for Python and summarize the results."
    ]

    for request in requests:
        print("\nUser:")
        print(request)

        plan = planner.plan(request)

        print("\nPlan:")
        print(plan)


if __name__ == "__main__":
    main()