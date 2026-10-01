from memory.profile import PersonalProfile
import os


def main():
    path = "sandbox/test_profile_clear.json"

    profile = PersonalProfile(path)

    profile.set_name("IRIS User")
    profile.set_preference("theme", "dark")
    profile.add_interest("AI")
    profile.add_note("project", "IRIS")

    print("Before clear:")
    print(profile.get_profile())

    profile.clear()

    print("\nAfter clear:")
    print(profile.get_profile())

    print("\nFile exists:", os.path.exists(path))


if __name__ == "__main__":
    main()
