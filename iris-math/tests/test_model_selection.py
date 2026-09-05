models = {
    "small": {
        "reasoning": 5,
        "speed": 10,
        "cost": 10
    },
    "medium": {
        "reasoning": 8,
        "speed": 7,
        "cost": 7
    },
    "large": {
        "reasoning": 10,
        "speed": 4,
        "cost": 3
    }
}


def select_model(task):
    requirements = {
        "simple": {
            "reasoning": 3,
            "speed": 8,
            "cost": 8
        },
        "coding": {
            "reasoning": 8,
            "speed": 6,
            "cost": 6
        },
        "complex": {
            "reasoning": 10,
            "speed": 3,
            "cost": 3
        }
    }

    required = requirements[task]

    best_model = None
    best_score = float("-inf")

    for name, model in models.items():
        score = (
            model["reasoning"] * required["reasoning"]
            + model["speed"] * required["speed"]
            + model["cost"] * required["cost"]
        )

        if score > best_score:
            best_score = score
            best_model = name

    return best_model, best_score


tasks = ["simple", "coding", "complex"]

for task in tasks:
    model, score = select_model(task)

    print(f"Task: {task}")
    print(f"Selected model: {model}")
    print(f"Score: {score}")
    print("-" * 40)