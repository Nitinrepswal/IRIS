
from core.computer_action_policy import ComputerActionPolicy


def main():
    policy = ComputerActionPolicy()

    assert policy.classify("move") == "low_risk"
    assert policy.classify("screen_inspection") == "low_risk"

    assert policy.classify("click") == "requires_confirmation"
    assert policy.classify("type") == "requires_confirmation"
    assert policy.classify("delete") == "requires_confirmation"
    assert policy.classify("submit") == "requires_confirmation"

    assert policy.classify("unknown") == "blocked"
    assert policy.classify("unrestricted_shell") == "blocked"
    assert policy.classify("") == "blocked"
    assert policy.classify(None) == "blocked"

    assert policy.requires_confirmation("click")
    assert policy.is_blocked("unknown")
    assert policy.is_allowed_without_confirmation("move")

    print("COMPUTER ACTION POLICY TEST: PASS")


if __name__ == "__main__":
    main()
