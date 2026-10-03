import time

from models.llm_model import LLMModel
from core.vision import VisionEngine
from tools.web_search import WebSearchTool
from tools.web_retriever import WebRetrieverTool


def measure(name, function):
    start = time.perf_counter()

    try:
        result = function()

        elapsed = time.perf_counter() - start

        print(f"{name}: {elapsed:.2f}s")

        return result

    except Exception as error:
        elapsed = time.perf_counter() - start

        print(f"{name}: FAILED after {elapsed:.2f}s")
        print(f"Error: {error}")

        return None


def main():
    print("IRIS Performance Benchmark")
    print("=" * 30)

    model = LLMModel()
    vision = VisionEngine()
    search = WebSearchTool()
    retriever = WebRetrieverTool()

    print("\nLLM")
    print("-" * 30)

    measure(
        "LLM response",
        lambda: model.generate(
            "Say hello in one short sentence."
        )
    )

    print("\nWeb")
    print("-" * 30)

    results = measure(
        "Web search",
        lambda: search.execute(
            "Python programming",
            limit=3
        )
    )

    if results:
        url = results[0].get("url")

        if url:
            measure(
                "Web retrieval",
                lambda: retriever.execute(url)
            )

    print("\nVision")
    print("-" * 30)

    image_path = "sandbox/screenshots/multimodal_screen.png"

    measure(
        "Vision analysis",
        lambda: vision.execute(image_path)
    )

    print("\nBenchmark complete.")


if __name__ == "__main__":
    main()