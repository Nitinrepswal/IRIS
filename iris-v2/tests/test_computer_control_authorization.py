
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

    backend = Mock()
    controller._backend = backend

    result = controller.move_mouse(100, 200)

    assert result["success"] is True, result
    permissions.check.assert_called_once_with("application")
    permissions.confirmation.confirm.assert_called_once_with("move")
    backend.moveTo.assert_called_once_with(100, 200)

    permissions.reset_mock()
    backend.reset_mock()
    permissions.check.return_value = False

    result = controller.type_text("Blocked text")

    assert result["success"] is False
    assert "permission denied" in result["message"].lower()
    backend.write.assert_not_called()
    backend.moveTo.assert_not_called()

    permissions.reset_mock()
    backend.reset_mock()
    permissions.check.return_value = True
    permissions.confirmation.confirm.return_value = False

    result = controller.press_key("enter")

    assert result["success"] is False
    assert "not approved" in result["message"].lower()
    permissions.confirmation.confirm.assert_called_once_with("press")
    backend.press.assert_not_called()

    print("COMPUTER CONTROL AUTHORIZATION TEST: PASS")


if __name__ == "__main__":
    main()
