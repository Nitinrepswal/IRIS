from core.iris_core import IRISCore


def main():
    iris = IRISCore()

    first_tool = object()
    second_tool = object()
    replacement_tool = object()

    iris.register_tool("search", first_tool)
    iris.register_tool("files", second_tool)

    assert iris.tools["search"] is first_tool
    assert iris.tools["files"] is second_tool

    iris.register_tool("search", replacement_tool)

    assert iris.tools["search"] is replacement_tool
    assert iris.tools["files"] is second_tool
    assert len(iris.tools) == 2

    print("DAY 296 IRIS CORE TOOLS TEST: PASS")


if __name__ == "__main__":
    main()