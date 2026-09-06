class ConversationMemory:
    def __init__(self, max_messages=6):
        self.messages = []
        self.max_messages = max_messages

    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_history(self):
        return self.messages


memory = ConversationMemory(max_messages=6)

memory.add("user", "My name is Nitin.")
memory.add("assistant", "Nice to meet you, Nitin.")

memory.add("user", "I am building an AI assistant.")
memory.add("assistant", "That's a great project.")

memory.add("user", "I am using Python.")
memory.add("assistant", "Python is a good choice.")

memory.add("user", "What language am I using?")


print("Conversation history:")

for message in memory.get_history():
    print(f"{message['role']}: {message['content']}")

print("\nTotal messages:")
print(len(memory.get_history()))