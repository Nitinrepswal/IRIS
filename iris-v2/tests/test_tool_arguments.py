from models.llm_model import LLMModel
from core.tool_arguments import ToolArgumentGenerator


def main():
    model = LLMModel()
    generator = ToolArgumentGenerator(model)

    requests = [
        (
            "Find my resume in the current directory.",
            "filesystem_search"
        ),
        (
            "Read my notes.txt file.",
            "file_reader"
        ),
        (
            "Create a file called hello.txt containing Hello IRIS.",
            "file_editor"
        ),
        (
            "Show me the files in this folder.",
            "terminal"
        )
    ]

    for message, tool in requests:
        result = generator.generate(message, tool)

        print("\nUser:", message)
        print("Tool:", result["tool"])
        print("Arguments:", result["arguments"])
        print("Reason:", result.get("reason", "No reason provided"))


if __name__ == "__main__":
    main()