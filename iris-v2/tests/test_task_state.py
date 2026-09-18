from core.task_state import TaskState


def main():
    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "resume"
        },
        {
            "step": 2,
            "action": "read",
            "target": "resume found in step 1"
        },
        {
            "step": 3,
            "action": "summarize",
            "target": "resume content"
        }
    ]

    state = TaskState(
        goal="Find and summarize the resume",
        tasks=tasks
    )

    print("Initial state:")
    print(state.get_state())

    state.start()

    print("\nAfter starting:")
    print(state.get_state())

    state.complete_step({
        "success": True,
        "message": "Resume found."
    })

    print("\nAfter step 1:")
    print(state.get_state())

    state.complete_step({
        "success": True,
        "message": "Resume read."
    })

    print("\nAfter step 2:")
    print(state.get_state())

    state.complete_step({
        "success": True,
        "message": "Resume summarized."
    })

    print("\nAfter step 3:")
    print(state.get_state())


if __name__ == "__main__":
    main()