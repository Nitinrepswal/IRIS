
from core.permission import PermissionSystem


def main():
    permissions = PermissionSystem()

    assert permissions.grant("unrestricted_shell") is False
    assert permissions.is_allowed("unrestricted_shell") is False

    assert permissions.grant("unknown") is False
    assert permissions.revoke("unknown") is False

    assert permissions.grant("filesystem") is True
    assert permissions.is_allowed("filesystem") is True

    assert permissions.revoke("filesystem") is True
    assert permissions.is_allowed("filesystem") is False

    assert permissions.grant(None) is False
    assert permissions.revoke(None) is False
    assert permissions.is_allowed(None) is False

    print("DAY 298 PERMISSION VALIDATION TEST: PASS")


if __name__ == "__main__":
    main()
