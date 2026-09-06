import json
import os


class IRISMemory:
    def __init__(self, file_path="memory_v1.json", max_messages=6):
        self.file_path = file_path
        self.max_messages = max_messages
        self.data = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)

        return {
            "conversation": [],
            "knowledge": {
                "preferences": [],
                "projects": [],
                "skills": []
            }
        }

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def add_message(self, role, content):
        self.data["conversation"].append({
            "role": role,
            "content": content
        })

        if len(self.data["conversation"]) > self.max_messages:
            self.data["conversation"] = self.data["conversation"][-self.max_messages:]

        self.save()

    def add_knowledge(self, category, information):
        if category not in self.data["knowledge"]:
            self.data["knowledge"][category] = []

        if information not in self.data["knowledge"][category]:
            self.data["knowledge"][category].append(information)

        self.save()

    def get_conversation(self):
        return self.data["conversation"]

    def get_knowledge(self, category):
        return self.data["knowledge"].get(category, [])

    def get_all(self):
        return self.data


memory = IRISMemory()

memory.add_message("user", "Hello IRIS.")
memory.add_message("assistant", "Hello! How can I help?")
memory.add_message("user", "I am building an AI assistant.")
memory.add_message("assistant", "That's a great project.")

memory.add_knowledge("projects", "User is building IRIS.")
memory.add_knowledge("skills", "User is learning AI engineering.")
memory.add_knowledge("preferences", "User prefers simple explanations.")


print("IRIS Memory V1")
print("=" * 40)

print("\nRecent conversation:")

for message in memory.get_conversation():
    print(f"{message['role']}: {message['content']}")

print("\nProjects:")

for project in memory.get_knowledge("projects"):
    print("-", project)

print("\nSkills:")

for skill in memory.get_knowledge("skills"):
    print("-", skill)

print("\nPreferences:")

for preference in memory.get_knowledge("preferences"):
    print("-", preference)

print("\nMemory file:")
print(os.path.abspath(memory.file_path))