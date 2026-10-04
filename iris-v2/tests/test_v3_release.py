from core.v3_release import V3Release


def main():
    print("IRIS V3.0 RELEASE VALIDATION")
    print("=" * 50)

    release = V3Release()

    result = release.validate()

    print("\nVersion:")
    print(result["version"])

    print("\nCodename:")
    print(result["codename"])

    print("\nPlatform:")
    print(result["platform"])

    print("\nCapabilities:")
    print(len(result["capabilities"]))

    print("\nPlugins:")
    for plugin in result["plugins"]:
        print("-", plugin)

    print("\nAdvanced tests:")
    print(
        f"{result['advanced_tests']['passed']}/"
        f"{result['advanced_tests']['total']}"
    )

    print("\nRuntime health:")
    print(result["health"]["status"])

    print("\nRelease ready:")
    print(result["release_ready"])

    assert result["version"] == "3.0.0"
    assert result["advanced_tests"]["release_ready"] is True
    assert result["health"]["status"] == "healthy"
    assert result["release_ready"] is True

    print("\n" + "=" * 50)
    print("DAY 198 TEST: PASS")


if __name__ == "__main__":
    main()