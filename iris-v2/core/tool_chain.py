
class ToolChainPlanner:
    ALLOWED_TOOLS = {
        "filesystem_search",
        "file_reader",
        "file_editor",
        "terminal",
        "browser",
        "web_search",
        "llm"
    }

    def build(self, tasks, dependencies):
        if not isinstance(tasks, list) or not isinstance(dependencies, list):
            return self._error("Tasks and dependencies must be lists.")

        task_map = {}

        for task in tasks:
            if not isinstance(task, dict):
                return self._error("Each task must be a dictionary.")

            step = task.get("step")
            action = task.get("action")
            target = task.get("target")
            tool = task.get("tool")

            if not isinstance(step, int) or isinstance(step, bool):
                return self._error("Each task needs an integer step.")

            if step in task_map:
                return self._error("Duplicate task step.")

            if not isinstance(action, str) or not action.strip():
                return self._error("Each task needs an action.")

            if not isinstance(target, str) or not target.strip():
                return self._error("Each task needs a target.")

            if tool not in self.ALLOWED_TOOLS:
                return self._error("Unsupported or missing tool.")

            task_map[step] = {
                "step": step,
                "action": action,
                "target": target,
                "tool": tool
            }

        dependency_map = {}

        for item in dependencies:
            if not isinstance(item, dict):
                return self._error("Each dependency must be a dictionary.")

            step = item.get("step")
            depends_on = item.get("depends_on")

            if step not in task_map or not isinstance(depends_on, list):
                return self._error("Invalid dependency entry.")

            if step in dependency_map:
                return self._error("Duplicate dependency entry.")

            if not all(
                isinstance(dep, int) and not isinstance(dep, bool)
                for dep in depends_on
            ):
                return self._error("Dependency steps must be integers.")

            if len(set(depends_on)) != len(depends_on):
                return self._error("Duplicate dependency reference.")

            for dep in depends_on:
                if dep not in task_map:
                    return self._error("Dependency references an unknown step.")

                if dep == step:
                    return self._error("A task cannot depend on itself.")

            dependency_map[step] = depends_on

        if set(dependency_map) != set(task_map):
            return self._error("Every task needs a dependency entry.")

        # Topological ordering: only schedule a task after its dependencies.
        remaining = set(task_map)
        completed = set()
        chain = []

        while remaining:
            ready = sorted(
                step
                for step in remaining
                if set(dependency_map[step]).issubset(completed)
            )

            if not ready:
                return self._error("Dependency cycle detected.")

            for step in ready:
                task = task_map[step]
                chain.append({
                    **task,
                    "depends_on": dependency_map[step].copy()
                })
                completed.add(step)
                remaining.remove(step)

        return {
            "valid": True,
            "chain": chain,
            "reason": "Tool chain planned successfully. No tools were executed."
        }

    def _error(self, reason):
        return {
            "valid": False,
            "chain": [],
            "reason": reason
        }
