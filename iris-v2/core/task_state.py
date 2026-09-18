class TaskState:
    def __init__(self, goal, tasks):
        self.goal = goal
        self.tasks = tasks
        self.current_step = 0
        self.status = "pending"
        self.results = []

    def start(self):
        self.status = "running"

    def complete_step(self, result):
        self.results.append(result)
        self.current_step += 1

        if self.current_step >= len(self.tasks):
            self.status = "completed"

    def fail_step(self, result):
        self.results.append(result)
        self.status = "failed"

    def get_current_task(self):
        if self.current_step >= len(self.tasks):
            return None

        return self.tasks[self.current_step]

    def get_state(self):
        return {
            "goal": self.goal,
            "status": self.status,
            "current_step": self.current_step,
            "total_steps": len(self.tasks),
            "results": self.results
        }