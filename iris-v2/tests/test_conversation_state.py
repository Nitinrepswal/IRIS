from models.llm_model import LLMModel
from core.conversation import ConversationLoop


def main():
    model = LLMModel()
    conversation = ConversationLoop(model, max_messages=4)

    conversation.chat("My name is Nitin.")
    conversation.chat("I am building an AI assistant called IRIS.")

    print("History after two exchanges:")
    print(conversation.get_history())

    print("\nNumber of messages:", len(conversation.get_history()))

    conversation.clear()

    print("\nHistory after clear:")
    print(conversation.get_history())


if __name__ == "__main__":
    main()