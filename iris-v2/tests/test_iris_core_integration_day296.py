from core.iris_core import IRISCore


class FakeModel:
    def generate(self, message):
        return f"Response: {message}"


class FakeMemory:
    pass


class FakeAgent:
    pass


def main():
    iris = IRISCore()
    model = FakeModel()
    memory = FakeMemory()
    agent = FakeAgent()
    tool = object()

    assert iris.process("Hello") == "IRIS model is not connected yet."

    iris.set_model(model)
    iris.set_memory(memory)
    iris.set_agent(agent)
    iris.register_tool("test", tool)

    assert iris.model is model
    assert iris.memory is memory
    assert iris.agent is agent
    assert iris.tools["test"] is tool
    assert iris.process("Hello IRIS") == "Response: Hello IRIS"

    print("DAY 296 IRIS CORE INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()