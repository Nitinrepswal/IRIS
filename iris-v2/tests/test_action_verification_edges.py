
from core.action_verification import ActionVerifier


def main():
    verifier = ActionVerifier()

    result = verifier.verify(None, {}, {})
    assert result["verified"] is False
    assert result["status"] == "failed"

    result = verifier.verify(
        {"type": "type", "text": "IRIS"},
        {"success": True, "dry_run": False},
        None
    )
    assert result["verified"] is False
    assert result["status"] == "unverified"

    result = verifier.verify(
        {"type": "type", "text": "IRIS"},
        {"success": True, "dry_run": False},
        {"text_present": True, "observed_text": "IRIS DAY 279"}
    )
    assert result["verified"] is True

    result = verifier.verify(
        {"type": "click"},
        {"success": True, "dry_run": False},
        {}
    )
    assert result["verified"] is False
    assert result["status"] == "unverified"

    print("ACTION VERIFICATION EDGE TEST: PASS")


if __name__ == "__main__":
    main()
