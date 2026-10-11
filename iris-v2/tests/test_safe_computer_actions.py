from core.computer_action_policy import ComputerActionPolicy


def main():
    policy = ComputerActionPolicy()

    assert policy.is_blocked("unknown")
    assert policy.is_blocked("unrestricted_shell")
    assert policy.is_blocked("disable_security")

    assert policy.requires_confirmation("delete")
    assert policy.requires_confirmation("submit")
    assert policy.requires_confirmation("send")
    assert policy.requires_confirmation("click")
    assert policy.requires_confirmation("type")

    assert policy.classify("move") == "low_risk"

    print("SAFE COMPUTER ACTIONS TEST: PASS")


if __name__ == "__main__":
    main()