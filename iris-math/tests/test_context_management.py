class ContextManager:

    def __init__(self, system_prompt, max_messages=4):
        self.system_prompt = system_prompt
        self.max_messages = max_messages
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_context(self):
        recent_messages = self.messages[-self.max_messages:]

        return [
            {
                "role": "system",
                "content": self.system_prompt
            },
            *recent_messages
        ]


context = ContextManager(
    system_prompt="You are IRIS, a helpful AI assistant.",
    max_messages=4
)

context.add_message("user", "My name is Nitin.")
context.add_message("assistant", "Nice to meet you, Nitin.")
context.add_message("user", "I am building an AI assistant.")
context.add_message("assistant", "That's a great project.")
context.add_message("user", "I am using Python.")
context.add_message("assistant", "Python is a good choice.")
context.add_message("user", "What language am I using?")

print("All messages:")
print(context.messages)

print("\nSelected context:")
for message in context.get_context():
    print(f"{message['role']}: {message['content']}")