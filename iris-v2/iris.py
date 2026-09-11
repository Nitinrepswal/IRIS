from models.llm_model import LLMModel
from core.conversation import ConversationLoop


def main():
    model = LLMModel()
    conversation = ConversationLoop(model)

    print("IRIS V2")
    print("Type 'exit' to quit.\n")

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            print("IRIS: Goodbye.")
            break

        response = conversation.chat(message)

        print("IRIS:", response)


if __name__ == "__main__":
    main()