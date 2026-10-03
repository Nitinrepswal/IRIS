from core.multi_step_executor import MultiStepExecutor
from core.observer import ObservationEngine
from core.recovery import RecoveryEngine
from core.task_state import TaskState


class AutonomousTaskEngine:
    def __init__(self, tool_layer, max_retries=2):
        self.executor = MultiStepExecutor(tool_layer)
        self.observer = ObservationEngine()
        self.recovery = RecoveryEngine(max_retries)

    def execute(self, goal, tasks):
        state = TaskState(goal, tasks)
        state.start()

        while state.status == "running":
            task = state.get_current_task()

            if task is None:
                break

            result = self._execute_task(task)

            observation = self.observer.observe(
                result["result"]
            )

            result["observation"] = observation

            if result["success"]:
                state.complete_step(result)
                continue

            state.fail_step(result)

        return state.get_state()

    def _execute_task(self, task):
        action = task["action"]
        target = task["target"]
        tool_name = task.get("tool")

        if tool_name is None:
            return {
                "step": task["step"],
                "success": False,
                "message": "No tool selected for task.",
                "result": {
                    "success": False,
                    "message": "No tool selected for task."
                }
            }

        arguments = self.executor._prepare_arguments(
            action,
            target
        )

        recovery = self.recovery.recover(
            self.executor.tool_layer.execute,
            tool_name,
            arguments
        )

        if recovery["success"]:
            return {
                "step": task["step"],
                "action": action,
                "target": target,
                "tool": tool_name,
                "success": True,
                "attempts": recovery["attempts"],
                "result": recovery["result"]
            }

        return {
            "step": task["step"],
            "action": action,
            "target": target,
            "tool": tool_name,
            "success": False,
            "attempts": recovery["attempts"],
            "result": recovery["result"]
        }