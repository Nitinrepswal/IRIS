class GoalTracker:
    def __init__(self, task_state):
        self.task_state = task_state

    def get_progress(self):
        total = len(self.task_state.tasks)

        if total == 0:
            return 100

        completed = self.task_state.current_step

        return int((completed / total) * 100)

    def get_status(self):
        status = self.task_state.status

        if status == "completed":
            return "completed"

        if status == "failed":
            return "failed"

        if status == "running":
            return "in_progress"

        return "pending"

    def get_goal_state(self):
        total = len(self.task_state.tasks)

        return {
            "goal": self.task_state.goal,
            "status": self.get_status(),
            "progress": self.get_progress(),
            "completed_steps": self.task_state.current_step,
            "total_steps": total
        }