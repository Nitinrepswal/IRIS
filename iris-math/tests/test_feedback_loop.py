class Agent:
    def __init__(self):
        self.tools = {
            "calculator": self.calculate,
            "weather": self.get_weather
        }

    def calculate(self, expression):
        return eval(expression)

    def get_weather(self, city):
        return f"Weather information for {city}"

    def execute(self, tool, argument):
        return self.tools[tool](argument)

    def observe(self, result):
        print("OBSERVATION:")
        print(result)

        if result:
            return "complete"

        return "continue"

    def run(self, tool, argument):
        print(f"Tool: {tool}")
        print(f"Argument: {argument}")

        result = self.execute(tool, argument)

        status = self.observe(result)

        print(f"Status: {status}")


agent = Agent()

agent.run("calculator", "25 * 4")

print("-" * 40)

agent.run("weather", "Delhi")