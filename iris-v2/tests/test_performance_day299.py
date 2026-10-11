
import statistics
import time


def benchmark(name, function, runs=3):
    times = []

    for index in range(runs):
        start = time.perf_counter()

        try:
            function()
        except Exception as error:
            print(f"{name} run {index + 1}: FAILED — {error}")
            continue

        elapsed = time.perf_counter() - start
        times.append(elapsed)
        print(f"{name} run {index + 1}: {elapsed:.2f}s")

    if not times:
        print(f"{name}: no successful runs")
        return

    print(f"{name} successful runs: {len(times)}/{runs}")
    print(f"{name} average: {statistics.mean(times):.2f}s")
    print(f"{name} median: {statistics.median(times):.2f}s")
    print(f"{name} fastest: {min(times):.2f}s")
    print(f"{name} slowest: {max(times):.2f}s")


def main():
    print("IRIS DAY 299 — REPEATED PERFORMANCE BENCHMARK")
    print("=" * 45)

    from models.llm_model import LLMModel
    from core.vision import VisionEngine
    from tools.web_search import WebSearchTool

    model = LLMModel()
    vision = VisionEngine()
    search = WebSearchTool()

    benchmark(
        "LLM",
        lambda: model.generate("Say hello in one short sentence."),
    )

    benchmark(
        "Web search",
        lambda: search.execute("Python programming", limit=3),
    )

    print("\nVision is omitted from repeated runs to avoid "
          "repeating the 65-second operation unnecessarily.")
    print("\nBenchmark complete.")


if __name__ == "__main__":
    main()
