from core.platform import PlatformManager
from core.plugin_manager import PluginManager


class IRISRelease:
    def __init__(self):
        self.version = "3.0.0"
        self.codename = "IRIS V3.0"

        self.platform = PlatformManager()

        self.plugins = PluginManager()
        self.plugins.load()

    def get_capabilities(self):
        return [
            "local_llm",
            "voice_input",
            "voice_output",
            "filesystem",
            "terminal",
            "web_browsing",
            "web_search",
            "system_tools",
            "memory",
            "planning",
            "autonomous_tasks",
            "vision",
            "multimodal_input",
            "plugins",
            "cloud_sync",
            "feedback"
        ]

    def get_plugins(self):
        return [
            plugin.name
            for plugin in self.plugins.list_plugins()
        ]

    def get_status(self):
        return {
            "version": self.version,
            "codename": self.codename,
            "platform": self.platform.get_platform(),
            "machine": self.platform.machine,
            "python": self.platform.python_version,
            "capabilities": self.get_capabilities(),
            "plugins": self.get_plugins(),
            "status": "release_candidate"
        }

    def is_ready(self):
        status = self.get_status()

        return (
            status["version"] == "3.0.0"
            and status["platform"] != "Unknown"
            and len(status["capabilities"]) > 0
        )