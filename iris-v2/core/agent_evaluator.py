class AgentEvaluator:
    def evaluate(self, task_state):
        total_steps = len(task_state.tasks)
        completed_steps = task_state.current_step

        failed = task_state.status == "failed"
        completed = task_state.status == "completed"

        if completed and completed_steps == total_steps:
            result = "success"
        elif failed:
            result = "failure"
        else:
            result = "incomplete"

        return {
            "goal": task_state.goal,
            "result": result,
            "completed_steps": completed_steps,
            "total_steps": total_steps,
            "success": result == "success"
        }