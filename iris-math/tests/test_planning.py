class Planner:
    def create_plan(self, intent, user_input):
        if intent == "weather":
            return [
                "Get weather information",
                "Check the weather result",
                "Return the weather to the user"
            ]

        if intent == "file":
            return [
                "Find the requested file",
                "Check the file",
                "Return the file information"
            ]

        if intent == "calculation":
            return [
                "Identify the numbers",
                "Perform the calculation",
                "Return the result"
            ]

        if intent == "question":
            return [
                "Understand the question",
                "Find relevant information",
                "Generate an answer"
            ]

        return [
            "Understand the request",
            "Determine how to respond"
        ]


planner = Planner()

requests = [
    ("weather", "What's the weather in Delhi?"),
    ("file", "Open my resume."),
    ("calculation", "Calculate 25 multiplied by 4."),
    ("question", "What is machine learning?"),
    ("unknown", "Tell me something interesting.")
]


print("IRIS Planning")
print("=" * 40)

for intent, request in requests:
    plan = planner.create_plan(intent, request)

    print(f"Request: {request}")
    print(f"Intent: {intent}")
    print("Plan:")

    for step, action in enumerate(plan, start=1):
        print(f"{step}. {action}")

    print("-" * 40)