import json
import os


class LongTermMemory:
    def __init__(self, file_path="memory.json"):
        self.file_path = file_path
        self.memories = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)

        return []

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.memories, file, indent=4)

    def add(self, memory):
        if memory not in self.memories:
            self.memories.append(memory)
            self.save()

    def get_all(self):
        return self.memories


memory = LongTermMemory()

memory.add("User is building IRIS.")
memory.add("User prefers simple explanations.")
memory.add("User is learning AI engineering.")

print("Long-term memories:")

for item in memory.get_all():
    print("-", item)

print("\nMemory file:")
print(os.path.abspath(memory.file_path))