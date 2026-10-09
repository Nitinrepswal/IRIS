
class ToolCapabilityRegistry:
    def __init__(self):
        self.capabilities = {
            "none": {
                "description": "Respond without executing a tool.",
                "actions": [
                    "conversation",
                    "explanation",
                    "general_question"
                ],
                "risk": "low",
                "requires_confirmation": False
            },
            "filesystem_search": {
                "description": "Find, list, and read files.",
                "actions": ["find", "search", "list", "read"],
                "risk": "medium",
                "requires_confirmation": False
            },
            "filesystem_edit": {
                "description": "Create or modify files.",
                "actions": ["create", "edit", "modify", "delete"],
                "risk": "high",
                "requires_confirmation": True
            },
            "memory": {
                "description": "Manage personal information stored in memory.",
                "actions": ["remember", "recall", "update", "forget"],
                "risk": "medium",
                "requires_confirmation": False
            },
            "terminal": {
                "description": "Execute terminal commands and scripts.",
                "actions": ["run_command", "run_script"],
                "risk": "high",
                "requires_confirmation": True
            },
            "browser": {
                "description": "Search the web and open webpages.",
                "actions": ["search_web", "open_url", "retrieve_page"],
                "risk": "low",
                "requires_confirmation": False
            },
            "application": {
                "description": "Open and interact with supported applications.",
                "actions": ["launch_application", "control_application"],
                "risk": "medium",
                "requires_confirmation": False
            },
            "system": {
                "description": "Retrieve operating system and system information.",
                "actions": ["system_info"],
                "risk": "low",
                "requires_confirmation": False
            }
        }

    def register(
        self,
        name,
        description,
        actions,
        risk="medium",
        requires_confirmation=False
    ):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Tool name must not be empty.")

        if not isinstance(description, str):
            raise ValueError("Description must be a string.")

        if risk not in {"low", "medium", "high"}:
            raise ValueError("Invalid risk level.")

        if not isinstance(actions, list):
            raise ValueError("Actions must be a list.")

        if not all(
            isinstance(action, str) and action.strip()
            for action in actions
        ):
            raise ValueError("Actions must contain non-empty strings.")

        if not isinstance(requires_confirmation, bool):
            raise ValueError("Confirmation must be a boolean.")

        self.capabilities[name] = {
            "description": description,
            "actions": actions.copy(),
            "risk": risk,
            "requires_confirmation": requires_confirmation
        }

    def get(self, name):
        capability = self.capabilities.get(name)

        if capability is None:
            return None

        return {
            **capability,
            "actions": capability["actions"].copy()
        }

    def list_tools(self):
        return list(self.capabilities.keys())

    def find_by_action(self, action):
        return [
            name
            for name, capability in self.capabilities.items()
            if action in capability["actions"]
        ]

    def get_all(self):
        return {
            name: {
                **capability,
                "actions": capability["actions"].copy()
            }
            for name, capability in self.capabilities.items()
        }
