class AgentMemory:
    def __init__(self):
        self.memory = {}

    def remember(self, key, value):
        self.memory[key] = value

    def recall(self, key):
        return self.memory.get(key, "Memory not found")


class IRISAgent:
    def __init__(self):
        self.memory = AgentMemory()

    def detect_intent(self, message):
        message = message.lower()

        if "weather" in message:
            return "weather"

        if "resume" in message or "file" in message:
            return "file"

        if "calculate" in message:
            return "calculation"

        if "what is" in message:
            return "question"

        return "unknown"

    def create_plan(self, intent):
        plans = {
            "weather": [
                "Understand weather request",
                "Get weather information",
                "Return weather result"
            ],
            "file": [
                "Understand file request",
                "Find requested file",
                "Return file information"
            ],
            "calculation": [
                "Understand calculation",
                "Perform calculation",
                "Return result"
            ],
            "question": [
                "Understand question",
                "Find relevant information",
                "Generate answer"
            ]
        }

        return plans.get(intent, [
            "Understand request",
            "Determine how to respond"
        ])

    def select_tool(self, intent):
        tools = {
            "weather": "weather_tool",
            "file": "file_tool",
            "calculation": "calculator_tool",
            "question": "knowledge_tool",
            "unknown": "no_tool"
        }

        return tools.get(intent, "no_tool")

    def execute_tool(self, tool, message):
        if tool == "calculator_tool":
            return 100

        if tool == "weather_tool":
            return "Weather information for Delhi"

        if tool == "file_tool":
            return "File found: resume.pdf"

        if tool == "knowledge_tool":
            return "Machine learning allows computers to learn patterns from data."

        return "No tool required"

    def run(self, message):
        print("USER")
        print(message)

        intent = self.detect_intent(message)

        print("\nINTENT")
        print(intent)

        plan = self.create_plan(intent)

        print("\nPLAN")
        for i, step in enumerate(plan, start=1):
            print(f"{i}. {step}")

        tool = self.select_tool(intent)

        print("\nTOOL")
        print(tool)

        observation = self.execute_tool(tool, message)

        print("\nOBSERVATION")
        print(observation)

        self.memory.remember("last_request", message)
        self.memory.remember("last_result", observation)

        print("\nMEMORY")
        print(f"last_request: {self.memory.recall('last_request')}")
        print(f"last_result: {self.memory.recall('last_result')}")

        print("\nFINAL ANSWER")
        print(observation)


agent = IRISAgent()

print("=" * 40)
print("IRIS AGENT V1")
print("=" * 40)

agent.run("Calculate 25 multiplied by 4.")