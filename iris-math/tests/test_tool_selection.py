class ToolSelector:
    def select_tool(self, action):
        action = action.lower()

        if "weather" in action:
            return "weather_tool"

        if "file" in action:
            return "file_tool"

        if "calculate" in action or "calculation" in action:
            return "calculator_tool"

        if "information" in action or "question" in action:
            return "knowledge_tool"

        if "answer" in action:
            return "llm_tool"

        return "no_tool"


selector = ToolSelector()

actions = [
    "Get weather information",
    "Find the requested file",
    "Perform the calculation",
    "Find relevant information",
    "Generate an answer",
    "Understand the request"
]


print("IRIS Tool Selection")
print("=" * 40)

for action in actions:
    tool = selector.select_tool(action)

    print(f"Action: {action}")
    print(f"Selected tool: {tool}")
    print("-" * 40)