
from core.tool_arguments import ToolArgumentGenerator


class MockModel:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def structured_chat(self, messages):
        if self.error:
            raise self.error
        return self.result


def main():
    print("IRIS DAY 220 ARGUMENT VALIDATION TEST")
    print("=" * 50)

    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    model = MockModel({
        "tool": "filesystem_search",
        "arguments": {
            "directory": ".",
            "query": "resume"
        },
        "reason": "Find the resume"
    })

    generator = ToolArgumentGenerator(model)

    result = generator.generate(
        "Find my resume in the current directory.",
        "filesystem_search"
    )

    check("Valid arguments accepted", result["valid"])

    check(
        "Expected arguments extracted",
        result["arguments"]["query"] == "resume"
    )

    check(
        "Current directory preserved",
        result["arguments"]["directory"] == "."
    )

    check(
        "Missing arguments list is empty",
        result["missing_arguments"] == []
    )

    model.result = {
        "tool": "file_reader",
        "arguments": {},
        "reason": "Read a file"
    }

    result = generator.generate("Read my file", "file_reader")

    check(
        "Missing path detected",
        result["missing_arguments"] == ["path"]
    )

    check(
        "Incomplete arguments marked invalid",
        result["valid"] is False
    )

    model.result = {
        "tool": "terminal",
        "arguments": {
            "command": "ls",
            "extra": "unsafe"
        },
        "reason": "List files"
    }

    result = generator.generate("List files", "terminal")

    check(
        "Unexpected arguments rejected",
        result["valid"] is False
    )

    model.result = {
        "tool": "file_reader",
        "arguments": {"path": 123},
        "reason": "Read file"
    }

    result = generator.generate("Read file", "file_reader")

    check(
        "Non-string argument values rejected",
        result["valid"] is False
    )

    model.result = {
        "tool": "terminal",
        "arguments": {"command": "ls"},
        "reason": "List files"
    }

    result = generator.generate("Run ls", "file_reader")

    check(
        "Mismatched tool rejected",
        result["valid"] is False
    )

    model.error = RuntimeError("Model unavailable")

    result = generator.generate(
        "Read notes.txt",
        "file_reader"
    )

    check(
        "Model failure handled safely",
        result["valid"] is False
        and result["arguments"] == {}
    )

    result = generator.generate("", "terminal")

    check(
        "Empty request rejected",
        result["valid"] is False
    )

    result = generator.generate("Do something", "unknown_tool")

    check(
        "Unsupported tool rejected",
        result["valid"] is False
    )

    print("\n" + "=" * 50)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("ARGUMENT VALIDATION: PASS")
    else:
        print("ARGUMENT VALIDATION: FAIL")


if __name__ == "__main__":
    main()
