class ApplicationTool:
    def __init__(self):
        self.application = {
            "status": "closed",
            "text": ""
        }

    def open_application(self):
        self.application["status"] = "open"
        return "Application opened"

    def write_text(self, text):
        if self.application["status"] != "open":
            return "Application is not open"

        self.application["text"] = text
        return f"Text written: {text}"

    def read_text(self):
        if self.application["status"] != "open":
            return "Application is not open"

        return self.application["text"]


class IRISApplicationAgent:
    def __init__(self):
        self.application = ApplicationTool()

    def run(self):
        print("USER")
        print("Open the application and write Hello IRIS.")

        print("\nSTEP 1")
        print("ACTION")
        print("open_application")

        observation = self.application.open_application()

        print("OBSERVATION")
        print(observation)

        print("\nSTEP 2")
        print("ACTION")
        print("write_text")

        observation = self.application.write_text("Hello IRIS.")

        print("OBSERVATION")
        print(observation)

        print("\nSTEP 3")
        print("ACTION")
        print("read_text")

        observation = self.application.read_text()

        print("OBSERVATION")
        print(observation)

        print("\nFINAL ANSWER")
        print("Application interaction completed.")


agent = IRISApplicationAgent()

print("=" * 40)
print("IRIS APPLICATION INTERACTION")
print("=" * 40)

agent.run()