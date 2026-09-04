def exact_match(actual, expected):
    return actual.strip().lower() == expected.strip().lower()


def contains_text(actual, expected):
    return expected.lower() in actual.lower()


def keyword_coverage(actual, keywords):
    actual = actual.lower()

    matched = 0

    for keyword in keywords:
        if keyword.lower() in actual:
            matched += 1

    return matched / len(keywords)


def iris_answer(question):
    answers = {
        "What is Python?":
            "Python is a high-level programming language.",

        "What is a list?":
            "A list is a collection that stores multiple values.",

        "What is a transformer?":
            "A transformer is a neural network architecture based on attention."
    }

    return answers.get(question, "I don't know.")


test_cases = [
    {
        "question": "What is Python?",
        "expected": "Python is a high-level programming language.",
        "keywords": ["Python", "programming language"]
    },
    {
        "question": "What is a list?",
        "expected": "A list is a collection that stores multiple values.",
        "keywords": ["list", "collection", "values"]
    },
    {
        "question": "What is a transformer?",
        "expected": "A transformer is a neural network architecture based on attention.",
        "keywords": ["transformer", "neural network", "attention"]
    }
]


exact_scores = []
contains_scores = []
coverage_scores = []


for test in test_cases:
    actual = iris_answer(test["question"])

    exact = exact_match(actual, test["expected"])
    contains = contains_text(actual, test["expected"])
    coverage = keyword_coverage(actual, test["keywords"])

    exact_scores.append(exact)
    contains_scores.append(contains)
    coverage_scores.append(coverage)

    print("Question:")
    print(test["question"])

    print("\nActual:")
    print(actual)

    print("\nExact match:")
    print(exact)

    print("Contains:")
    print(contains)

    print("Keyword coverage:")
    print(round(coverage, 2))

    print("\n" + "-" * 40)


exact_accuracy = sum(exact_scores) / len(exact_scores)
contains_accuracy = sum(contains_scores) / len(contains_scores)
average_coverage = sum(coverage_scores) / len(coverage_scores)


print("\nEvaluation Summary:")
print("Exact match accuracy:", round(exact_accuracy, 2))
print("Contains accuracy:", round(contains_accuracy, 2))
print("Average keyword coverage:", round(average_coverage, 2))