class IntentDetector:
    def detect(self, user_input):
        text = user_input.lower()

        if "weather" in text or "temperature" in text:
            return "weather"

        if "open" in text or "file" in text or "document" in text:
            return "file"

        if "calculate" in text or "sum" in text or "multiply" in text:
            return "calculation"

        if "what is" in text or "explain" in text or "define" in text:
            return "question"

        return "unknown"


detector = IntentDetector()

requests = [
    "What's the weather in Delhi?",
    "Open my resume.",
    "Calculate 25 multiplied by 4.",
    "What is machine learning?",
    "Tell me something interesting."
]


print("IRIS Intent Detection")
print("=" * 40)

for request in requests:
    intent = detector.detect(request)

    print(f"Request: {request}")
    print(f"Intent: {intent}")
    print("-" * 40)