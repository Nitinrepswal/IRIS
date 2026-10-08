from models.llm_model import LLMModel


def main():
    print("IRIS V3.1 PROMPT OPTIMIZATION TEST")
    print("=" * 55)

    model = LLMModel()

    prompt = model.system_prompt

    print("\nPrompt length:")
    print(len(prompt), "characters")

    print("\nIdentity checks:")

    checks = {
        "IRIS identity": "You are IRIS" in prompt,
        "Nitin creator": "Nitin" in prompt,
        "Qwen model": "Qwen 2.5 3B" in prompt,
        "Local assistant": "local AI assistant" in prompt,
        "Behavior rules": "BEHAVIOR:" in prompt,
        "Capabilities": "CAPABILITIES:" in prompt
    }

    for name, result in checks.items():
        print(
            f"{name}:",
            "PASS" if result else "FAIL"
        )

    passed = all(checks.values())

    print("\nPrompt structure:")

    sections = [
        "IDENTITY:",
        "IDENTITY QUESTIONS:",
        "CAPABILITIES:",
        "BEHAVIOR:"
    ]

    for section in sections:
        found = section in prompt

        print(
            f"{section}",
            "PASS" if found else "FAIL"
        )

        passed = passed and found

    print("\n" + "=" * 55)

    if passed:
        print("PROMPT OPTIMIZATION TEST: PASS")
    else:
        print("PROMPT OPTIMIZATION TEST: FAIL")


if __name__ == "__main__":
    main()