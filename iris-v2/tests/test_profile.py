from memory.profile import PersonalProfile


def main():
    profile = PersonalProfile("sandbox/test_profile.json")

    profile.set_name("IRIS User")
    profile.set_preference("theme", "dark")
    profile.add_interest("AI")
    profile.add_interest("Python")
    profile.add_note("project", "IRIS")

    print("Name:", profile.get_name())
    print("Theme:", profile.get_preference("theme"))
    print("Interests:", profile.get_interests())
    print("Project:", profile.get_note("project"))

    print("\nFull profile:")
    print(profile.get_profile())


if __name__ == "__main__":
    main()