class AgentMemory:
    def __init__(self):
        self.memory = {}

    def remember(self, key, value):
        self.memory[key] = value

    def recall(self, key):
        return self.memory.get(key, "Memory not found")

    def show_memory(self):
        print("Agent Memory")
        print("============")
        for key, value in self.memory.items():
            print(f"{key}: {value}")


class Agent:
    def __init__(self):
        self.memory = AgentMemory()

    def process(self, message):
        message = message.lower()

        if "what is my project" in message:
            return f"Your project is {self.memory.recall('project')}."

        if "what language" in message:
            return f"You are using {self.memory.recall('language')}."

        if "project" in message:
            self.memory.remember("project", "IRIS")
            return "I will remember that your project is IRIS."

        if "using python" in message:
            self.memory.remember("language", "Python")
            return "I will remember that you are using Python."

        return "I don't have enough information."


agent = Agent()

print("USER: My project is IRIS.")
print("IRIS:", agent.process("My project is IRIS."))

print("\nUSER: I am using Python.")
print("IRIS:", agent.process("I am using Python."))

print("\nUSER: What is my project?")
print("IRIS:", agent.process("What is my project?"))

print("\nUSER: What language am I using?")
print("IRIS:", agent.process("What language am I using?"))

print()
agent.memory.show_memory()