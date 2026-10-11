from core.action_verification import ActionVerifier


def main():
    verifier = ActionVerifier()

    action = {"type": "type", "text": "Hello IRIS"}
    execution = {"success": True, "dry_run": False}

    verified = verifier.verify(
        action,
        execution,
        {
            "text_present": True,
            "observed_text": "Hello IRIS"
        }
    )
    assert verified["status"] == "verified"

    unverified = verifier.verify(
        action,
        execution,
        {
            "text_present": False,
            "observed_text": ""
        }
    )
    assert unverified["status"] == "unverified"

    failed = verifier.verify(
        action,
        {"success": False, "message": "Execution failed"},
        {}
    )
    assert failed["status"] == "failed"

    simulated = verifier.verify(
        action,
        {"success": True, "dry_run": True},
        {}
    )
    assert simulated["status"] == "dry_run"

    print("DAY 283 ACTION VERIFICATION TEST: PASS")


if __name__ == "__main__":
    main()