class MultiStepAgent:
    def __init__(self):
        self.steps = []
        self.observations = []

    def add_step(self, tool, argument):
        self.steps.append({
            "tool": tool,
            "argument": argument
        })

    def execute_tool(self, tool, argument):
        if tool == "calculator":
            return eval(argument)

        if tool == "text":
            return f"Result received: {argument}"

        return "Unknown tool"

    def run(self):
        for i, step in enumerate(self.steps, start=1):
            print(f"\nSTEP {i}")
            print(f"Tool: {step['tool']}")
            print(f"Argument: {step['argument']}")

            result = self.execute_tool(
                step["tool"],
                step["argument"]
            )

            self.observations.append(result)

            print(f"Observation: {result}")

        print("\nFINAL RESULT")
        print(self.observations[-1])


agent = MultiStepAgent()

agent.add_step("calculator", "25 * 4")
agent.add_step("text", "100")

agent.run()