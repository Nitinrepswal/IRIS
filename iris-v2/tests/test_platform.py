from core.platform import PlatformManager


def main():
    platform_manager = PlatformManager()

    print("Platform:", platform_manager.get_platform())
    print("System:", platform_manager.system)
    print("Machine:", platform_manager.machine)
    print("Python:", platform_manager.python_version)

    print("\nPlatform checks:")

    print("macOS:", platform_manager.is_macos())
    print("Windows:", platform_manager.is_windows())
    print("Linux:", platform_manager.is_linux())


if __name__ == "__main__":
    main()