from core.computer_action_policy import ComputerActionPolicy


def main():
    policy = ComputerActionPolicy()

    dangerous_actions = [
        "unknown",
        "unrestricted_shell",
        "disable_security"
    ]

    for action in dangerous_actions:
        assert policy.is_blocked(action), action

    sensitive_actions = [
        "delete",
        "send",
        "submit",
        "click",
        "type"
    ]

    for action in sensitive_actions:
        assert policy.requires_confirmation(action), action

    print("DAY 286 COMPUTER ACTION SAFETY TEST: PASS")


if __name__ == "__main__":
    main()