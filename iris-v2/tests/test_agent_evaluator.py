from core.task_state import TaskState
from core.agent_evaluator import AgentEvaluator


def main():
    evaluator = AgentEvaluator()

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "resume"
        },
        {
            "step": 2,
            "action": "read",
            "target": "resume"
        },
        {
            "step": 3,
            "action": "summarize",
            "target": "resume"
        }
    ]

    state = TaskState(
        goal="Find and summarize the resume",
        tasks=tasks
    )

    state.start()

    state.complete_step({
        "success": True,
        "message": "Resume found."
    })

    state.complete_step({
        "success": True,
        "message": "Resume read."
    })

    state.complete_step({
        "success": True,
        "message": "Resume summarized."
    })

    print("Successful task:")
    print(evaluator.evaluate(state))

    failed_state = TaskState(
        goal="Find the resume",
        tasks=[
            {
                "step": 1,
                "action": "search",
                "target": "resume"
            }
        ]
    )

    failed_state.start()

    failed_state.fail_step({
        "success": False,
        "message": "Resume not found."
    })

    print("\nFailed task:")
    print(evaluator.evaluate(failed_state))


if __name__ == "__main__":
    main()