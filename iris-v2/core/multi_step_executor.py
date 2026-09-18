import re


class MultiStepExecutor:
    def __init__(self, tool_layer):
        self.tool_layer = tool_layer

    def execute(self, tasks):
        results = []

        for task in tasks:
            action = task["action"]
            target = task["target"]

            tool_name, arguments = self._prepare_tool(
                action,
                target
            )

            if tool_name is None:
                results.append({
                    "step": task["step"],
                    "success": False,
                    "message": f"Unsupported action: {action}"
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
                "result": result
            })

            if not result["success"]:
                break

        return results

    def _prepare_tool(self, action, target):
        if action == "search":
            query = self._extract_search_query(target)

            return (
                "filesystem_search",
                {
                    "directory": ".",
                    "query": query
                }
            )

        if action == "read":
            return (
                "file_reader",
                {
                    "path": target
                }
            )

        if action == "create":
            return (
                "file_editor",
                {
                    "path": target,
                    "content": ""
                }
            )

        return None, {}

    def _extract_search_query(self, target):
        quoted = re.search(
            r"'([^']+)'|\"([^\"]+)\"",
            target
        )

        if quoted:
            return quoted.group(1) or quoted.group(2)

        return target