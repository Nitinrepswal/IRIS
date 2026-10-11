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

    permissions.check.return_value = True
    permissions.confirmation.confirm.return_value = False

    result = controller.click_mouse(100, 200)

    assert result["success"] is False
    assert "not approved" in result["message"].lower()
    backend.moveTo.assert_not_called()
    backend.click.assert_not_called()

    permissions.reset_mock()
    backend.reset_mock()

    permissions.check.return_value = True
    permissions.confirmation.confirm.return_value = True

    result = controller._perform("unknown")

    assert result["success"] is False
    assert result["message"] == "Unsupported action"
    permissions.check.assert_not_called()
    permissions.confirmation.confirm.assert_not_called()
    backend.assert_not_called()

    print("DAY 291 COMPUTER CONTROL SAFETY TEST: PASS")


if __name__ == "__main__":
    main()