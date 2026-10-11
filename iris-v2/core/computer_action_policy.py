
class ComputerActionPolicy:
    def __init__(self):
        self.low_risk_actions = {
            "screen_inspection",
            "move"
        }

        self.confirmation_actions = {
            "click",
            "type",
            "press",
            "computer_control",
            "terminal",
            "filesystem",
            "mouse",
            "keyboard",
            "delete",
            "send",
            "submit"
        }

        self.blocked_actions = {
            "unknown",
            "disable_security",
            "unrestricted_shell"
        }

    def classify(self, action):
        if not isinstance(action, str) or not action.strip():
            return "blocked"

        action = action.strip().lower()

        if action in self.blocked_actions:
            return "blocked"

        if action in self.low_risk_actions:
            return "low_risk"

        if action in self.confirmation_actions:
            return "requires_confirmation"

        return "blocked"

    def is_allowed_without_confirmation(self, action):
        return self.classify(action) == "low_risk"

    def requires_confirmation(self, action):
        return self.classify(action) == "requires_confirmation"

    def is_blocked(self, action):
        return self.classify(action) == "blocked"
