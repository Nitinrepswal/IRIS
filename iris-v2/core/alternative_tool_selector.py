
from core.tool_capabilities import ToolCapabilityRegistry


class AlternativeToolSelector:
    ALTERNATIVES = {
        "filesystem_search": ["browser", "terminal"],
        "filesystem_edit": ["terminal"],
        "file_reader": ["filesystem_search", "terminal"],
        "file_editor": ["terminal"],
        "browser": ["terminal"],
        "terminal": ["browser", "system"],
        "memory": [],
        "application": ["terminal"],
        "system": ["terminal"]
    }

    FAILURE_BLOCKS = {
        "permission_denied": True,
        "invalid_arguments": True,
        "missing_arguments": True,
        "file_not_found": True,
        "tool_not_found": False,
        "timeout": False,
        "connection_error": False,
        "execution_error": False,
        "unknown_error": True
    }

    def __init__(self, registry=None):
        self.registry = registry or ToolCapabilityRegistry()

    def select(self, failed_tool, failure_category, available_tools=None):
        if not isinstance(failed_tool, str) or not failed_tool.strip():
            return self._result(False, None, "Failed tool name is invalid.")

        if not isinstance(failure_category, str) or not failure_category.strip():
            return self._result(False, None, "Failure category is invalid.")

        failed_tool = failed_tool.strip()
        failure_category = failure_category.strip().lower()

        if failure_category not in self.FAILURE_BLOCKS:
            return self._result(False, None, "Unknown failure category.")

        if self.FAILURE_BLOCKS[failure_category]:
            return self._result(
                True,
                None,
                "The failure needs correction before choosing an alternative."
            )

        if available_tools is None:
            available_tools = self.registry.list_tools()

        if not isinstance(available_tools, list):
            return self._result(False, None, "Available tools must be a list.")

        if not all(isinstance(tool, str) for tool in available_tools):
            return self._result(False, None, "Tool names must be strings.")

        registered = set(self.registry.list_tools())
        available = set(available_tools)

        if not available.issubset(registered):
            return self._result(
                False,
                None,
                "Available tools contain unregistered names."
            )

        candidates = self.ALTERNATIVES.get(failed_tool, [])

        for candidate in candidates:
            if candidate == failed_tool:
                continue

            if candidate not in available:
                continue

            capability = self.registry.get(candidate)

            if capability is None:
                continue

            return self._result(
                True,
                candidate,
                "Alternative recommended; compatibility and permissions must be checked."
            )

        return self._result(
            True,
            None,
            "No registered alternative is available."
        )

    def _result(self, valid, tool, reason):
        return {
            "valid": valid,
            "alternative": tool,
            "reason": reason,
            "execute": False
        }
