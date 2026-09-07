import platform
import sys


class SystemInfoTool:
    def get_system_info(self):
        return {
            "operating_system": platform.system(),
            "os_version": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version.split()[0]
        }


class IRISSystemAgent:
    def __init__(self):
        self.system = SystemInfoTool()

    def run(self):
        print("USER")
        print("What system am I running on?")

        print("\nACTION")
        print("get_system_information")

        information = self.system.get_system_info()

        print("\nOBSERVATION")

        for key, value in information.items():
            print(f"{key}: {value}")

        print("\nFINAL ANSWER")
        print(
            f"You are running {information['operating_system']} "
            f"on a {information['machine']} machine "
            f"with Python {information['python_version']}."
        )


agent = IRISSystemAgent()

print("=" * 40)
print("IRIS SYSTEM INFORMATION")
print("=" * 40)

agent.run()