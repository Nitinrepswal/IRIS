
class PermissionSystem:
    def __init__(self):
        self.permissions = {
            "browser": True,
            "system": True,
            "application": True,
            "filesystem": True,
            "terminal": False,
        }

    def is_allowed(self, action):
        if not isinstance(action, str):
            return False
        return self.permissions.get(action, False)

    def grant(self, action):
        if not isinstance(action, str) or action not in self.permissions:
            return False
        self.permissions[action] = True
        return True

    def revoke(self, action):
        if not isinstance(action, str) or action not in self.permissions:
            return False
        self.permissions[action] = False
        return True

    def get_permissions(self):
        return self.permissions.copy()
