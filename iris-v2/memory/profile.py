import json
import os


class PersonalProfile:
    def __init__(self, path="memory/profile.json"):
        self.path = path

        directory = os.path.dirname(self.path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        self.profile = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return {
                "name": "",
                "preferences": {},
                "interests": [],
                "notes": {}
            }

        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.profile, file, indent=2)

    def set_name(self, name):
        self.profile["name"] = name
        self.save()

    def get_name(self):
        return self.profile.get("name", "")

    def set_preference(self, key, value):
        self.profile["preferences"][key] = value
        self.save()

    def get_preference(self, key):
        return self.profile["preferences"].get(key)

    def add_interest(self, interest):
        if interest not in self.profile["interests"]:
            self.profile["interests"].append(interest)
            self.save()

    def get_interests(self):
        return self.profile.get("interests", [])

    def add_note(self, key, value):
        self.profile["notes"][key] = value
        self.save()

    def get_note(self, key):
        return self.profile["notes"].get(key)

    def get_profile(self):
        return self.profile.copy()