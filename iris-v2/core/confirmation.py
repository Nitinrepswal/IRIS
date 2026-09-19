class ConfirmationSystem:
    def __init__(self):
        self.risky_actions = {
            "terminal",
            "application",
            "filesystem"
        }

        self.blocked_actions = {
            "unknown"
        }

    def requires_confirmation(self, action):
        return action in self.risky_actions

    def is_blocked(self, action):
        return action in self.blocked_actions

    def confirm(self, action):
        if self.is_blocked(action):
            return False

        if not self.requires_confirmation(action):
            return True

        answer = input(
            f"IRIS wants to perform '{action}'. "
            "Allow? (y/n): "
        )

        return answer.strip().lower() == "y"