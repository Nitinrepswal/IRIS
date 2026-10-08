from models.llm_model import LLMModel


def main():
    print("IRIS V3.1 LLM OPTIMIZATION TEST")
    print("=" * 50)

    model = LLMModel()

    normal = model.benchmark()

    print("\nNormal generation:")
    print("Response:", normal["response"])
    print("Time:", normal["time"], "seconds")

    fast = model.benchmark_fast()

    print("\nFast generation:")
    print("Response:", fast["response"])
    print("Time:", fast["time"], "seconds")

    improvement = (
        normal["time"] - fast["time"]
    )

    print("\nPerformance difference:")
    print(
        "Difference:",
        round(improvement, 3),
        "seconds"
    )

    passed = (
        bool(normal["response"])
        and bool(fast["response"])
        and normal["time"] > 0
        and fast["time"] > 0
    )

    print("\n" + "=" * 50)

    if passed:
        print("LLM OPTIMIZATION TEST: PASS")
    else:
        print("LLM OPTIMIZATION TEST: FAIL")


if __name__ == "__main__":
    main()