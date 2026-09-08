from core.iris_core import IRISCore
from models.llm_model import LLMModel


def main():
    iris = IRISCore()

    model = LLMModel()
    iris.set_model(model)

    print("IRIS V2")
    print("Type 'exit' to quit.\n")

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            print("IRIS: Goodbye.")
            break

        response = iris.process(message)

        print("IRIS:", response)


if __name__ == "__main__":
    main()