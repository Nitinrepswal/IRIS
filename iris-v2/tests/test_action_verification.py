
from core.action_verification import ActionVerifier


def main():
    verifier = ActionVerifier()

    result = verifier.verify(
        action={"type": "type", "text": "Hello IRIS"},
        execution_result={
            "success": True,
            "dry_run": False,
            "action": "type"
        },
        observation={"text_present": True, "observed_text": "Hello IRIS"}
    )

    assert result["verified"] is True
    assert result["status"] == "verified"

    result = verifier.verify(
        action={"type": "type", "text": "Hello IRIS"},
        execution_result={
            "success": True,
            "dry_run": False,
            "action": "type"
        },
        observation={"text_present": False, "observed_text": ""}
    )

    assert result["verified"] is False
    assert result["status"] == "unverified"

    result = verifier.verify(
        action={"type": "click"},
        execution_result={
            "success": False,
            "message": "Permission denied"
        },
        observation={}
    )

    assert result["verified"] is False
    assert result["status"] == "failed"

    result = verifier.verify(
        action={"type": "type", "text": "Hello IRIS"},
        execution_result={
            "success": True,
            "dry_run": True,
            "action": "type"
        },
        observation={"text_present": True, "observed_text": "Hello IRIS"}
    )

    assert result["verified"] is False
    assert result["status"] == "dry_run"

    print("ACTION VERIFICATION TEST: PASS")


if __name__ == "__main__":
    main()
