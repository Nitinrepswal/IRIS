from core.feedback import FeedbackSystem


def main():
    feedback = FeedbackSystem(
        path="sandbox/test_feedback.json"
    )

    feedback.clear()

    first = feedback.add(
        "Hello IRIS",
        5,
        "Very helpful"
    )

    second = feedback.add(
        "Open calculator",
        4,
        "Worked correctly"
    )

    print("Feedback entries:")
    for entry in feedback.get_all():
        print(entry)

    print("\nAverage rating:")
    print(feedback.get_average_rating())

    assert len(feedback.get_all()) == 2
    assert feedback.get_average_rating() == 4.5

    feedback.clear()

    print("\nFeedback cleared.")
    print("Entries:", feedback.get_all())

    assert feedback.get_all() == []


if __name__ == "__main__":
    main()