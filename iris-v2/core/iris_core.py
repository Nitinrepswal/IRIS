class IRISCore:
    def __init__(self):
        self.model = None
        self.memory = None
        self.tools = {}
        self.agent = None

    def set_model(self, model):
        self.model = model

    def set_memory(self, memory):
        self.memory = memory

    def register_tool(self, name, tool):
        self.tools[name] = tool

    def set_agent(self, agent):
        self.agent = agent

    def process(self, message):
        if self.model is None:
            return "IRIS model is not connected yet."

        return self.model.generate(message)