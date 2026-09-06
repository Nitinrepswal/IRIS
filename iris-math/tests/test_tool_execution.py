class ToolExecutor:
    def __init__(self):
        self.tools = {
            "calculator_tool": self.calculate,
            "weather_tool": self.get_weather,
            "file_tool": self.find_file
        }

    def calculate(self, expression):
        return eval(expression)

    def get_weather(self, city):
        return f"Weather information for {city}"

    def find_file(self, filename):
        return f"File found: {filename}"

    def execute(self, tool_name, argument):
        if tool_name not in self.tools:
            return "Tool not found"

        return self.tools[tool_name](argument)


executor = ToolExecutor()

requests = [
    ("calculator_tool", "25 * 4"),
    ("weather_tool", "Delhi"),
    ("file_tool", "resume.pdf")
]


print("IRIS Tool Execution")
print("=" * 40)

for tool, argument in requests:
    result = executor.execute(tool, argument)

    print(f"Tool: {tool}")
    print(f"Argument: {argument}")
    print(f"Result: {result}")
    print("-" * 40)