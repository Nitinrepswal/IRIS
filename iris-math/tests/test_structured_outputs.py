import json


def parse_response(response):
    data = json.loads(response)

    required_fields = [
        "answer",
        "confidence",
        "category"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing field: {field}")

    if not isinstance(data["answer"], str):
        raise ValueError("answer must be a string")

    if not isinstance(data["confidence"], (int, float)):
        raise ValueError("confidence must be a number")

    if not isinstance(data["category"], str):
        raise ValueError("category must be a string")

    return data


response = """
{
    "answer": "Python lists store multiple values.",
    "confidence": 0.95,
    "category": "programming"
}
"""


result = parse_response(response)

print("Parsed response:")
print(result)

print("\nAnswer:")
print(result["answer"])

print("\nConfidence:")
print(result["confidence"])

print("\nCategory:")
print(result["category"])