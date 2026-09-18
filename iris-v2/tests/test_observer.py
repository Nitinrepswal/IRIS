from core.observer import ObservationEngine


def main():
    observer = ObservationEngine()

    results = [
        {
            "success": True,
            "result": ["resume.pdf", "resume_old.pdf"]
        },
        {
            "success": True,
            "result": []
        },
        {
            "success": True,
            "result": "Resume content"
        },
        {
            "success": False,
            "message": "File not found."
        }
    ]

    for index, result in enumerate(results, start=1):
        observation = observer.observe(result)

        print(f"\nResult {index}:")
        print("Status:", observation["status"])
        print("Message:", observation["message"])


if __name__ == "__main__":
    main()