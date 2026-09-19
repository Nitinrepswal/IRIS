class PermissionSystem:
    def __init__(self):
        self.permissions = {
            "browser": True,
            "system": True,
            "application": True,
            "filesystem": True,
            "terminal": False
        }

    def is_allowed(self, action):
        return self.permissions.get(
            action,
            False
        )

    def grant(self, action):
        self.permissions[action] = True

    def revoke(self, action):
        self.permissions[action] = False

    def get_permissions(self):
        return self.permissions.copy()