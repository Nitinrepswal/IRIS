from tests.test_iris_core import IRISCore


def main():
    iris = IRISCore()

    print("IRIS V1")
    print("Type 'exit' to quit.\n")

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            print("IRIS: Goodbye.")
            break

        result = iris.process(message)

        if result["intent"] == "chat":
            print("IRIS:", result["response"])

        elif result["intent"] == "memory":
            print("IRIS memory:", result["memory"])

        elif result["intent"] == "filesystem":
            print("IRIS files:", result["result"])

        elif result["intent"] == "system":
            print("IRIS system:", result["result"])


if __name__ == "__main__":
    main()