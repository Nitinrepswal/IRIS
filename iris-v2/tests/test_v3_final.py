from core.final_release import FinalRelease


def main():
    print("IRIS V3.0 FINAL RELEASE")
    print("=" * 60)

    release = FinalRelease()
    result = release.run()

    print("\nRelease information")
    print("-" * 60)
    print("Version:", result["version"])
    print("Codename:", result["codename"])
    print("Platform:", result["platform"])

    print("\nValidation")
    print("-" * 60)
    print("Success:", result["success"])
    print("Release ready:", result["release_ready"])

    if "error" in result:
        print("Error:", result["error"])

    assert result["success"] is True
    assert result["version"] == "3.0.0"
    assert result["codename"] == "IRIS V3.0"
    assert result["release_ready"] is True

    print("\n" + "=" * 60)
    print("IRIS V3.0 FINAL RELEASE: PASS")
    print("DAY 200: COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()