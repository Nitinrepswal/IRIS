
from core.tool_result_interpreter import ToolResultInterpreter


class MockModel:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error

    def structured_chat(self, messages):
        if self.error:
            raise self.error
        return self.response


def main():
    print("IRIS DAY 225 TOOL RESULT INTERPRETATION TEST")
    print("=" * 55)

    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    interpreter = ToolResultInterpreter()

    result = interpreter.interpret(
        "filesystem_search",
        {"success": True, "result": ["resume.pdf", "notes.txt"], "retry": False}
    )

    check("Successful result accepted", result["valid"] and result["success"])
    check("Raw result preserved", result["data"] == ["resume.pdf", "notes.txt"])
    check("List result summarized", "2 item(s)" in result["summary"])

    result = interpreter.interpret(
        "file_reader",
        {"success": True, "result": "Hello IRIS", "retry": False}
    )

    check("String result preserved", result["data"] == "Hello IRIS")
    check("String result summarized", result["summary"] == "Hello IRIS")

    result = interpreter.interpret(
        "terminal",
        {
            "success": False,
            "error": "execution_error",
            "message": "Command failed",
            "retry": True
        }
    )

    check("Failure result recognized", result["valid"] and not result["success"])
    check("Failure message preserved", result["summary"] == "Command failed")
    check("Retry flag preserved", result["retry"] is True)

    result = interpreter.interpret(
        "filesystem_search",
        {"success": True, "result": [], "retry": False}
    )

    check("Empty results handled", "empty collection" in result["summary"])

    result = interpreter.interpret("terminal", "invalid result")

    check("Invalid result structure rejected", result["valid"] is False)

    model = MockModel({"summary": "Found two relevant files."})
    interpreter = ToolResultInterpreter(model)

    result = interpreter.interpret(
        "filesystem_search",
        {"success": True, "result": ["resume.pdf", "notes.txt"]}
    )

    check("Model interpretation accepted",
          result["summary"] == "Found two relevant files.")

    model = MockModel(error=RuntimeError("Model unavailable"))
    interpreter = ToolResultInterpreter(model)

    result = interpreter.interpret(
        "filesystem_search",
        {"success": True, "result": ["resume.pdf"]}
    )

    check("Model failure uses safe fallback",
          result["valid"] and result["data"] == ["resume.pdf"])

    print("\n" + "=" * 55)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("TOOL RESULT INTERPRETATION: PASS")
    else:
        print("TOOL RESULT INTERPRETATION: FAIL")


if __name__ == "__main__":
    main()
