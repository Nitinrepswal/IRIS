from core.permission_control import PermissionControl


def main():
    controller = PermissionControl()

    print("Initial permissions:")
    print(controller.get_permissions())

    print()
    print("Application allowed:")
    print(
        controller.check("application")
    )

    print()
    print("Filesystem allowed:")
    print(
        controller.check("file")
    )

    print()
    print("Browser allowed:")
    print(
        controller.check("web")
    )

    print()
    print("System allowed:")
    print(
        controller.check("system")
    )

    print()
    print("Revoking filesystem permission...")

    controller.revoke("filesystem")

    print(
        "Filesystem allowed:",
        controller.check("file")
    )

    print()
    print("Granting filesystem permission...")

    controller.grant("filesystem")

    print(
        "Filesystem allowed:",
        controller.check("file")
    )


if __name__ == "__main__":
    main()