
from unittest.mock import Mock

from core.mouse_keyboard import MouseKeyboardController


def main():
    permissions = Mock()
    backend = Mock()

    controller = MouseKeyboardController(
        dry_run=False,
        permission_control=permissions
    )
    controller._backend = backend

    # Permission check failure must block execution.
    permissions.check.side_effect = RuntimeError(
        "Permission service failed"
    )

    result = controller.press_key("enter")

    assert result["success"] is False
    assert "Permission check failed" in result["message"]
    backend.press.assert_not_called()

    # Confirmation failure must also block execution.
    permissions.reset_mock()
    backend.reset_mock()

    permissions.check.side_effect = None
    permissions.check.return_value = True
    permissions.confirmation.confirm.side_effect = RuntimeError(
        "Confirmation service failed"
    )

    result = controller.type_text("Do not type this")

    assert result["success"] is False
    assert "Confirmation failed" in result["message"]
    backend.write.assert_not_called()

    # When confirmation is explicitly disabled, execution is allowed
    # if permission is granted.
    permissions.reset_mock()
    backend.reset_mock()

    permissions.check.side_effect = None
    permissions.check.return_value = True

    controller = MouseKeyboardController(
        dry_run=False,
        permission_control=permissions,
        require_confirmation=False
    )
    controller._backend = backend

    result = controller.press_key("enter")

    assert result["success"] is True
    backend.press.assert_called_once_with("enter")
    permissions.confirmation.confirm.assert_not_called()

    print("COMPUTER CONTROL AUTHORIZATION EDGE TEST: PASS")


if __name__ == "__main__":
    main()
