from unittest.mock import patch

from core.human_approval import HumanApproval


def main():
    approval = HumanApproval()

    with patch("builtins.input", return_value="y"):
        assert approval.request("click") is True

    with patch("builtins.input", return_value="n"):
        assert approval.request("delete") is False

    with patch("builtins.input", return_value="yes"):
        assert approval.request("submit") is False

    assert approval.request("") is False
    assert approval.request(None) is False

    print("DAY 285 HUMAN APPROVAL TEST: PASS")


if __name__ == "__main__":
    main()