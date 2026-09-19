import os
import platform
import shutil
import sys

from tools.tool import Tool


class SystemTool(Tool):
    def __init__(self):
        super().__init__(
            name="system",
            description="Provides safe information about the current system."
        )

    def execute(self):
        disk = shutil.disk_usage("/")

        return {
            "operating_system": platform.system(),
            "os_version": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version.split()[0],
            "current_directory": os.getcwd(),
            "disk_total_gb": round(
                disk.total / (1024 ** 3),
                2
            ),
            "disk_free_gb": round(
                disk.free / (1024 ** 3),
                2
            )
        }