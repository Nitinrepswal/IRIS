from core.permission_control import PermissionControl


def main():
    controller = PermissionControl()

    assert controller.requires_confirmation("click") is True
    assert controller.requires_confirmation("type") is True
    assert controller.requires_confirmation("terminal") is True

    assert controller.requires_confirmation("unknown") is False
    assert controller.requires_confirmation("move") is False

    print("PERMISSION POLICY INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()