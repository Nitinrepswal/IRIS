from core.permission import PermissionSystem


def main():
    permissions = PermissionSystem()

    print("IRIS Permission System")

    print("\nInitial permissions:")

    for action, allowed in permissions.get_permissions().items():
        print(f"{action}: {allowed}")

    print("\nTerminal permission:")

    print(
        "Allowed:",
        permissions.is_allowed("terminal")
    )

    print("\nGranting terminal permission...")

    permissions.grant("terminal")

    print(
        "Allowed:",
        permissions.is_allowed("terminal")
    )

    print("\nRevoking terminal permission...")

    permissions.revoke("terminal")

    print(
        "Allowed:",
        permissions.is_allowed("terminal")
    )

    print("\nUnknown action:")

    print(
        "Allowed:",
        permissions.is_allowed("unknown")
    )


if __name__ == "__main__":
    main()