import time


models = {
    "small": {
        "reasoning": 5,
        "speed": 10,
        "cost": 10
    },
    "medium": {
        "reasoning": 8,
        "speed": 7,
        "cost": 7
    },
    "large": {
        "reasoning": 10,
        "speed": 4,
        "cost": 3
    }
}


def select_model(task):
    if task == "simple":
        return "small"
    elif task == "coding":
        return "medium"
    else:
        return "large"


def build_prompt(question, history):
    prompt = "You are IRIS, a helpful AI assistant.\n\n"

    for message in history:
        prompt += f"{message['role']}: {message['content']}\n"

    prompt += f"user: {question}\nassistant:"

    return prompt


def generate_response(question):
    responses = {
        "what is python?":
            "Python is a high-level programming language.",
        "what is a transformer?":
            "A transformer is a neural network architecture based on attention.",
        "what is a list?":
            "A list is a collection that stores multiple values."
    }

    return responses.get(
        question.lower(),
        "I am IRIS. I can help you learn programming and AI."
    )


def stream_response(response):
    for word in response.split():
        print(word, end=" ", flush=True)
        time.sleep(0.2)


history = []

question = input("You: ")

task = "simple"
model = select_model(task)

prompt = build_prompt(question, history)
response = generate_response(question)

history.append({
    "role": "user",
    "content": question
})

history.append({
    "role": "assistant",
    "content": response
})

print(f"\nModel: {model}")
print("\nIRIS: ", end="")

stream_response(response)

print("\n\nPrompt:")
print(prompt)

print("\nConversation history:")
for message in history:
    print(f"{message['role']}: {message['content']}")