from core.plugin_manager import PluginManager


def main():
    manager = PluginManager()
    manager.load()

    print("Loaded plugins:")

    for plugin in manager.list_plugins():
        print(f"- {plugin.name}: {plugin.description}")

    result = manager.execute(
        "hello",
        "IRIS plugin system works"
    )

    print("\nPlugin result:")
    print(result)

    assert "hello" in manager.plugins
    assert result["success"] is True


if __name__ == "__main__":
    main()