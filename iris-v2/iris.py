from core.iris_core import IRISCore
from models.test_model import TestModel


def main():
    iris = IRISCore()

    model = TestModel()
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