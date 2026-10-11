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
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Tool name must be a non-empty string")

        if tool is None:
            raise ValueError("Tool cannot be None")

        self.tools[name.strip()] = tool

    def set_agent(self, agent):
        self.agent = agent

    def process(self, message):
        if self.model is None:
            return "IRIS model is not connected yet."

        return self.model.generate(message)