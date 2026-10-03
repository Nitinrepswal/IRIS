from core.web_knowledge import WebKnowledge


def main():
    knowledge = WebKnowledge()

    question = "What is Python programming language?"

    result = knowledge.execute(question)

    print("Success:", result["success"])

    if result["success"]:
        print("\nIRIS answer:")
        print(result["answer"])
    else:
        print("\nError:")
        print(result["message"])


if __name__ == "__main__":
    main()