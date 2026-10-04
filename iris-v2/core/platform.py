import platform


class PlatformManager:
    def __init__(self):
        self.system = platform.system()
        self.machine = platform.machine()
        self.python_version = platform.python_version()

    def is_macos(self):
        return self.system == "Darwin"

    def is_windows(self):
        return self.system == "Windows"

    def is_linux(self):
        return self.system == "Linux"

    def get_platform(self):
        if self.is_macos():
            return "macOS"

        if self.is_windows():
            return "Windows"

        if self.is_linux():
            return "Linux"

        return "Unknown"

    def get_info(self):
        return {
            "platform": self.get_platform(),
            "system": self.system,
            "machine": self.machine,
            "python": self.python_version
        }