from core.iris_core import IRISCore


def main():
    iris = IRISCore()

    for name in ("", "   ", None, 123):
        try:
            iris.register_tool(name, object())
        except ValueError:
            pass
        else:
            raise AssertionError(f"Invalid tool name accepted: {name!r}")

    try:
        iris.register_tool("search", None)
    except ValueError:
        pass
    else:
        raise AssertionError("None tool was accepted")

    tool = object()
    iris.register_tool(" search ", tool)

    assert iris.tools == {"search": tool}

    existing_tool = iris.tools["search"]

    try:
        iris.register_tool("search", None)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid replacement was accepted")

    assert iris.tools["search"] is existing_tool

    print("DAY 296 IRIS CORE VALIDATION TEST: PASS")


if __name__ == "__main__":
    main()