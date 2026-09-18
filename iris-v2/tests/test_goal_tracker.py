from core.task_state import TaskState
from core.goal_tracker import GoalTracker


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
            "target": "resume"
        },
        {
            "step": 3,
            "action": "summarize",
            "target": "resume"
        },
        {
            "step": 4,
            "action": "save",
            "target": "summary"
        }
    ]

    state = TaskState(
        goal="Find and process the resume",
        tasks=tasks
    )

    tracker = GoalTracker(state)

    print("Initial goal state:")
    print(tracker.get_goal_state())

    state.start()

    state.complete_step({
        "success": True,
        "message": "Resume found."
    })

    print("\nAfter step 1:")
    print(tracker.get_goal_state())

    state.complete_step({
        "success": True,
        "message": "Resume read."
    })

    print("\nAfter step 2:")
    print(tracker.get_goal_state())

    state.complete_step({
        "success": True,
        "message": "Resume summarized."
    })

    print("\nAfter step 3:")
    print(tracker.get_goal_state())

    state.complete_step({
        "success": True,
        "message": "Summary saved."
    })

    print("\nAfter step 4:")
    print(tracker.get_goal_state())


if __name__ == "__main__":
    main()