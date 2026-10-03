from core.health import IRISHealth


def main():
    health = IRISHealth()

    print("IRIS V2.4 Health Check")
    print("=" * 30)

    result = health.check_all()

    print("\nOverall status:")
    print(result["status"])

    print("\nComponents:")

    for name, status in result["components"].items():
        print(f"\n{name}:")
        print(status)


if __name__ == "__main__":
    main()