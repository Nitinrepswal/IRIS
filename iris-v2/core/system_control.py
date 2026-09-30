from core.computer_control import ComputerControl


class SystemControl:
    def __init__(self):
        self.computer = ComputerControl()

    def information(self):
        return self.computer.system_information()

    def execute(self, message):
        text = message.lower().strip()

        system_commands = {
            "system information",
            "system info",
            "computer information",
            "computer info",
            "my system",
            "about my computer"
        }

        if text not in system_commands:
            return None

        info = self.information()

        return (
            f"Operating System: "
            f"{info['operating_system']} "
            f"{info['os_version']}\n"
            f"Machine: {info['machine']}\n"
            f"Processor: {info['processor']}\n"
            f"Python: {info['python_version']}\n"
            f"Current Directory: "
            f"{info['current_directory']}\n"
            f"Disk Total: {info['disk_total_gb']} GB\n"
            f"Disk Free: {info['disk_free_gb']} GB"
        )