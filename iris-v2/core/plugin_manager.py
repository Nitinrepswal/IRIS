import importlib
import os


class PluginManager:
    def __init__(self, plugin_directory="plugins"):
        self.plugin_directory = plugin_directory
        self.plugins = {}

    def register(self, plugin):
        self.plugins[plugin.name] = plugin

    def load(self):
        if not os.path.exists(self.plugin_directory):
            return

        for filename in os.listdir(self.plugin_directory):
            if not filename.endswith("_plugin.py"):
                continue

            module_name = filename[:-3]
            module = importlib.import_module(
                f"{self.plugin_directory}.{module_name}"
            )

            for value in module.__dict__.values():
                if isinstance(value, type):
                    if hasattr(value, "name") and hasattr(value, "execute"):
                        if value.__name__ == "Plugin":
                            continue

                        self.register(value())

    def get(self, name):
        return self.plugins.get(name)

    def list_plugins(self):
        return list(self.plugins.values())

    def execute(self, name, message):
        plugin = self.get(name)

        if plugin is None:
            return {
                "success": False,
                "message": f"Plugin not found: {name}"
            }

        return plugin.execute(message)