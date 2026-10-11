
from core.task_state import TaskState


def main():
    state = TaskState("Test task state", [])

    assert state.status == "pending"
    assert state.current_step == 0
    assert state.get_current_task() is None

    state.start()
    assert state.status == "running"

    empty_state = state.get_state()
    assert empty_state["total_steps"] == 0
    assert empty_state["results"] == []

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "example",
        },
        {
            "step": 2,
            "action": "read",
            "target": "example.txt",
        },
    ]

    state = TaskState("Test task progression", tasks)
    state.start()

    first_result = {
        "step": 1,
        "success": True,
    }
    state.complete_step(first_result)

    assert state.current_step == 1
    assert state.status == "running"
    assert state.get_current_task() == tasks[1]

    second_result = {
        "step": 2,
        "success": True,
    }
    state.complete_step(second_result)

    assert state.current_step == 2
    assert state.status == "completed"
    assert state.get_current_task() is None
    assert len(state.get_state()["results"]) == 2

    print("DAY 297 TASK STATE TEST: PASS")


if __name__ == "__main__":
    main()
