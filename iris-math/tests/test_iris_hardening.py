from test_iris_core import IRISCore


def test_chat():
    iris = IRISCore()

    result = iris.process("Hello IRIS")

    assert result["intent"] == "chat"
    assert "response" in result


def test_filesystem():
    iris = IRISCore()

    result = iris.process("Show me the files")

    assert result["intent"] == "filesystem"
    assert result["tool"] == "list_files"
    assert isinstance(result["result"], list)


def test_system():
    iris = IRISCore()

    result = iris.process("What system am I using?")

    assert result["intent"] == "system"
    assert result["tool"] == "system_info"
    assert "system" in result["result"]
    assert "architecture" in result["result"]


def test_memory():
    iris = IRISCore()

    iris.process("Hello IRIS")
    result = iris.process("Remember this")

    assert result["intent"] == "memory"
    assert "Hello IRIS" in result["memory"]
    assert "Remember this" in result["memory"]


def test_unknown_tool():
    iris = IRISCore()

    result = iris.execute_tool("unknown_tool")

    assert result == "Tool not available"


def test_empty_message():
    iris = IRISCore()

    result = iris.process("")

    assert result["intent"] == "chat"


def test_case_handling():
    iris = IRISCore()

    result = iris.process("WHAT FILES ARE HERE?")

    assert result["intent"] == "filesystem"


def test_memory_limit():
    iris = IRISCore()

    for i in range(10):
        iris.process(f"Message {i}")

    memory = iris.retrieve_memory()

    assert len(memory) == 5
    assert memory[-1] == "Message 9"


def run_tests():
    tests = [
        test_chat,
        test_filesystem,
        test_system,
        test_memory,
        test_unknown_tool,
        test_empty_message,
        test_case_handling,
        test_memory_limit
    ]

    passed = 0

    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1
        except Exception as error:
            print(f"FAIL: {test.__name__} -> {error}")

    total = len(tests)
    accuracy = passed / total

    print()
    print(f"Tests passed: {passed}/{total}")
    print(f"Pass rate: {accuracy:.2%}")

    return passed == total


if __name__ == "__main__":
    run_tests()