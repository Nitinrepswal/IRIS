import json
import os


class PersonalKnowledgeBase:
    def __init__(self, file_path="knowledge_base.json"):
        self.file_path = file_path
        self.data = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)

        return {
            "preferences": [],
            "projects": [],
            "skills": []
        }

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def add(self, category, information):
        if category not in self.data:
            self.data[category] = []

        if information not in self.data[category]:
            self.data[category].append(information)
            self.save()

    def get_category(self, category):
        return self.data.get(category, [])

    def get_all(self):
        return self.data


knowledge = PersonalKnowledgeBase()

knowledge.add("preferences", "User prefers simple explanations.")
knowledge.add("preferences", "User prefers practical examples.")

knowledge.add("projects", "User is building IRIS.")
knowledge.add("projects", "IRIS is an AI assistant.")

knowledge.add("skills", "User is learning Python.")
knowledge.add("skills", "User is learning AI engineering.")


print("Personal Knowledge Base:")

for category, items in knowledge.get_all().items():
    print(f"\n{category}:")

    for item in items:
        print("-", item)

print("\nProjects:")
for project in knowledge.get_category("projects"):
    print("-", project)

print("\nKnowledge base file:")
print(os.path.abspath(knowledge.file_path))