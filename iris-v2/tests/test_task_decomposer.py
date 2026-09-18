from models.llm_model import LLMModel
from core.task_decomposer import TaskDecomposer


def main():
    model = LLMModel()
    decomposer = TaskDecomposer(model)

    messages = [
        "Find my resume and read it.",
        "Find my resume, read it, and summarize it.",
        "Create a file called hello.txt and write Hello IRIS in it."
    ]

    for message in messages:
        result = decomposer.decompose(message)

        print("\nUser:", message)
        print("Goal:", result["goal"])
        print("Tasks:")

        for task in result["tasks"]:
            print(
                f"{task['step']}. "
                f"Action: {task['action']} | "
                f"Target: {task['target']}"
            )


if __name__ == "__main__":
    main()