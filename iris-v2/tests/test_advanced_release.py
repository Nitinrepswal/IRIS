from core.advanced_release import AdvancedRelease


def main():
    release = AdvancedRelease()

    print("IRIS V2.4 Advanced Release")
    print("=" * 35)

    results = release.run()

    print("\nLLM:")
    print(results["llm"])

    print("\nVision:")
    print(results["vision"])

    print("\nWeb Knowledge:")
    print(results["web"])

    print("\nMultimodal:")
    print(results["multimodal"])

    print("\nRelease validation:")
    print(
        f"{results['passed']}/{results['total']} tests passed"
    )

    print(
        "Performance OK:",
        results["performance_ok"]
    )

    print(
        "Release ready:",
        results["release_ready"]
    )


if __name__ == "__main__":
    main()