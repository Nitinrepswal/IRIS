from core.permission_control import PermissionControl


def main():
    controller = PermissionControl()

    assert controller.check("unknown") is False
    assert controller.check("terminal") is False

    assert controller.requires_confirmation("click") is True
    assert controller.requires_confirmation("delete") is True

    assert controller.confirmation.is_blocked("unknown") is True
    assert controller.confirmation.is_blocked("unrestricted_shell") is True
    assert controller.confirmation.is_blocked("disable_security") is True

    controller.revoke("filesystem")
    assert controller.check("file") is False

    controller.grant("filesystem")
    assert controller.check("file") is True

    print("DAY 290 PERMISSION ENFORCEMENT TEST: PASS")


if __name__ == "__main__":
    main()