
from unittest.mock import Mock

from core.mouse_keyboard import MouseKeyboardController


def main():
    permissions = Mock()
    permissions.check.return_value = True
    permissions.confirmation.confirm.return_value = True

    controller = MouseKeyboardController(
        dry_run=True,
        permission_control=permissions,
        require_confirmation=False,
    )

    result = controller.type_text("Security audit")

    assert result["success"] is True
    assert result["dry_run"] is True
    permissions.check.assert_called_once_with("application")
    permissions.confirmation.confirm.assert_not_called()

    print("DAY 298 CONFIRMATION BYPASS AUDIT: PASS")


if __name__ == "__main__":
    main()
