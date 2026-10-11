
from core.computer_action_policy import ComputerActionPolicy


class ConfirmationSystem:
    def __init__(self):
        self.policy = ComputerActionPolicy()

    def requires_confirmation(self, action):
        return self.policy.requires_confirmation(action)

    def is_blocked(self, action):
        return self.policy.is_blocked(action)

    def confirm(self, action):
        if not isinstance(action, str) or not action.strip():
            return False

        action = action.strip().lower()

        if self.is_blocked(action):
            return False

        if not self.requires_confirmation(action):
            return True

        answer = input(
            f"IRIS wants to perform '{action}'. "
            "Allow? (y/n): "
        )

        return answer.strip().lower() == "y"
