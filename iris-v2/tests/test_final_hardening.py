from core.final_release import FinalRelease


def main():
    print("IRIS V3.0 FINAL HARDENING")
    print("=" * 50)

    release = FinalRelease()

    result = release.run()

    print("\nVersion:")
    print(result["version"])

    print("\nCodename:")
    print(result["codename"])

    print("\nPlatform:")
    print(result["platform"])

    print("\nValidation success:")
    print(result["success"])

    print("\nRelease ready:")
    print(result["release_ready"])

    if "error" in result:
        print("\nError:")
        print(result["error"])

    assert result["success"] is True
    assert result["version"] == "3.0.0"
    assert result["codename"] == "IRIS V3.0"
    assert result["release_ready"] is True

    assert release.is_ready() is True

    print("\n" + "=" * 50)
    print("DAY 199 TEST: PASS")


if __name__ == "__main__":
    main()