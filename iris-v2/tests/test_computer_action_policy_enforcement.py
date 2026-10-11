
from unittest.mock import Mock

from core.mouse_keyboard import MouseKeyboardController


def main():
    permissions = Mock()
    permissions.check.return_value = True
    permissions.confirmation.confirm.return_value = True

    controller = MouseKeyboardController(
        dry_run=False,
        permission_control=permissions
    )
    controller._backend = Mock()

    result = controller._perform("unknown")

    assert result["success"] is False
    assert result["message"] == "Unsupported action"
    permissions.check.assert_not_called()
    permissions.confirmation.confirm.assert_not_called()
    controller._backend.assert_not_called()
    controller._backend.moveTo.assert_not_called()
    controller._backend.click.assert_not_called()
    controller._backend.write.assert_not_called()
    controller._backend.press.assert_not_called()

    print("COMPUTER ACTION POLICY ENFORCEMENT TEST: PASS")


if __name__ == "__main__":
    main()
