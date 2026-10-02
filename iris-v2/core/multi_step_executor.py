class MultiStepExecutor:
    def __init__(self, tool_layer):
        self.tool_layer = tool_layer

    def execute(self, tasks):
        results = []

        for task in tasks:
            action = task["action"]
            target = task["target"]
            tool_name = task.get("tool")

            arguments = self._prepare_arguments(
                action,
                target
            )

            if tool_name is None:
                results.append({
                    "step": task["step"],
                    "success": False,
                    "message": "No tool selected for task."
                })
                continue

            result = self.tool_layer.execute(
                tool_name,
                arguments
            )

            results.append({
                "step": task["step"],
                "action": action,
                "target": target,
                "tool": tool_name,
                "result": result
            })

            if not result["success"]:
                break

        return results

    def _prepare_arguments(self, action, target):
        if action == "search":
            return {
                "directory": ".",
                "query": target
            }

        if action == "read":
            return {
                "path": target
            }

        if action == "create":
            return {
                "path": target,
                "content": ""
            }

        if action == "edit":
            return {
                "path": target,
                "content": ""
            }

        return {
            "input": target
        }