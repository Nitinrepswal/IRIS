
from unittest.mock import patch

from core.confirmation import ConfirmationSystem
from core.permission_control import PermissionControl


def main():
    confirmation = ConfirmationSystem()

    risky_actions = [
        "terminal",
        "filesystem",
        "mouse",
        "keyboard",
        "computer_control",
        "delete",
        "send",
        "submit"
    ]

    for action in risky_actions:
        assert confirmation.requires_confirmation(action)

    assert confirmation.is_blocked("unknown")
    assert confirmation.confirm("unknown") is False
    assert confirmation.confirm("") is False

    with patch("builtins.input", return_value="n"):
        assert confirmation.confirm("mouse") is False

    with patch("builtins.input", return_value="y"):
        assert confirmation.confirm("mouse") is True

    permissions = PermissionControl()

    assert permissions.check("application") is True
    assert permissions.check("invalid_tool") is False

    permissions.revoke("application")
    assert permissions.check("application") is False

    print("COMPUTER ACTION SAFETY TEST: PASS")


if __name__ == "__main__":
    main()
