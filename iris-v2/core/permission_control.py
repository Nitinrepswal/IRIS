from core.permission import PermissionSystem
from core.confirmation import ConfirmationSystem


class PermissionControl:
    def __init__(self):
        self.permissions = PermissionSystem()
        self.confirmation = ConfirmationSystem()

    def is_allowed(self, action):
        return self.permissions.is_allowed(
            action
        )

    def grant(self, action):
        self.permissions.grant(
            action
        )

    def revoke(self, action):
        self.permissions.revoke(
            action
        )

    def get_permissions(self):
        return self.permissions.get_permissions()

    def get_action(self, tool):
        actions = {
            "application": "application",
            "file": "filesystem",
            "web": "browser",
            "system": "system"
        }

        return actions.get(tool)

    def check(self, tool):
        action = self.get_action(tool)

        if action is None:
            return False

        return self.is_allowed(action)

    def requires_confirmation(self, action):
        return self.confirmation.requires_confirmation(
            action
        )