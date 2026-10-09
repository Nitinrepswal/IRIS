
class ToolDependencyDetector:
    def detect(self, tasks):
        if not isinstance(tasks, list):
            return {
                "valid": False,
                "dependencies": [],
                "reason": "Tasks must be a list."
            }

        step_ids = []

        for task in tasks:
            if not isinstance(task, dict):
                return {
                    "valid": False,
                    "dependencies": [],
                    "reason": "Each task must be a dictionary."
                }

            step = task.get("step")

            if not isinstance(step, int) or isinstance(step, bool):
                return {
                    "valid": False,
                    "dependencies": [],
                    "reason": "Each task needs an integer step."
                }

            if step in step_ids:
                return {
                    "valid": False,
                    "dependencies": [],
                    "reason": "Duplicate step numbers are not allowed."
                }

            step_ids.append(step)

        dependencies = []

        for index, task in enumerate(tasks):
            step = task["step"]
            target = task.get("target", "")
            action = task.get("action", "")

            if not isinstance(target, str) or not isinstance(action, str):
                return {
                    "valid": False,
                    "dependencies": [],
                    "reason": "Task action and target must be strings."
                }

            depends_on = []

            for previous in tasks[:index]:
                previous_step = previous["step"]
                reference = f"step {previous_step}"

                if reference in target.lower():
                    depends_on.append(previous_step)

            dependencies.append({
                "step": step,
                "depends_on": list(dict.fromkeys(depends_on))
            })

        return {
            "valid": True,
            "dependencies": dependencies,
            "reason": "Dependencies detected from explicit step references."
        }
