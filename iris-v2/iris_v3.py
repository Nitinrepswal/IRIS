from core.final_release import FinalRelease


def main():
    print("IRIS V3.0")
    print("=" * 50)
    print("Final release validation")
    print()

    release = FinalRelease()
    result = release.run()

    print("Version:", result["version"])
    print("Codename:", result["codename"])
    print("Platform:", result["platform"])
    print("Validation success:", result["success"])
    print("Release ready:", result["release_ready"])

    if "error" in result:
        print("Error:", result["error"])

    print()
    print("=" * 50)

    if release.is_ready():
        print("IRIS V3.0 RELEASE: READY")
        return

    print("IRIS V3.0 RELEASE: NOT READY")


if __name__ == "__main__":
    main()