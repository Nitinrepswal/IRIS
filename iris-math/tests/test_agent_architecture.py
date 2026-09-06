class Agent:
    def __init__(self):
        self.memory = []
        self.tools = []
        self.planner = None

    def receive(self, user_input):
        print("USER:")
        print(user_input)

    def reason(self, user_input):
        print("\nREASONING:")
        print("IRIS is analyzing the user's request.")

    def plan(self, user_input):
        print("\nPLANNER:")
        print("A plan will be created here.")

    def act(self):
        print("\nACTION:")
        print("IRIS will use a tool here.")

    def observe(self):
        print("\nOBSERVATION:")
        print("IRIS will inspect the result here.")

    def run(self, user_input):
        self.receive(user_input)
        self.reason(user_input)
        self.plan(user_input)
        self.act()
        self.observe()


agent = Agent()

agent.run("Find the weather in Delhi.")