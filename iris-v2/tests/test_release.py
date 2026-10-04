from core.release import IRISRelease


def main():
    release = IRISRelease()

    status = release.get_status()

    print("IRIS RELEASE")
    print("=" * 40)

    print("Version:", status["version"])
    print("Codename:", status["codename"])
    print("Platform:", status["platform"])
    print("Machine:", status["machine"])
    print("Python:", status["python"])

    print("\nCapabilities:")

    for capability in status["capabilities"]:
        print("-", capability)

    print("\nPlugins:")

    for plugin in status["plugins"]:
        print("-", plugin)

    print("\nRelease ready:")
    print(release.is_ready())

    assert status["version"] == "3.0.0"
    assert status["codename"] == "IRIS V3.0"
    assert status["platform"] != "Unknown"
    assert len(status["capabilities"]) > 0
    assert release.is_ready() is True

    print("\nDAY 197 TEST: PASS")


if __name__ == "__main__":
    main()