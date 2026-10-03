from core.advanced_release import AdvancedRelease
from core.health import IRISHealth


def main():
    print("IRIS V2.4 FINAL RELEASE")
    print("=" * 40)

    print("\n1. Advanced Release Validation")
    print("-" * 40)

    release = AdvancedRelease()
    release_result = release.run()

    print(
        f"Tests: "
        f"{release_result['passed']}/"
        f"{release_result['total']}"
    )

    print(
        "Performance OK:",
        release_result["performance_ok"]
    )

    print(
        "Release ready:",
        release_result["release_ready"]
    )

    print("\n2. Runtime Health Check")
    print("-" * 40)

    health = IRISHealth()
    health_result = health.check_all()

    print(
        "Overall status:",
        health_result["status"]
    )

    for name, result in health_result["components"].items():
        print(f"{name}: {result}")

    release_passed = release_result["release_ready"]
    health_passed = health_result["status"] == "healthy"

    final_status = release_passed and health_passed

    print("\n" + "=" * 40)
    print("IRIS V2.4 FINAL STATUS")
    print("=" * 40)

    print("Release validation:", release_passed)
    print("Runtime health:", health_passed)
    print("V2.4 READY:", final_status)


if __name__ == "__main__":
    main()