
from core.tool_capabilities import ToolCapabilityRegistry


def main():
    print("IRIS TOOL CAPABILITY REGISTRY TEST")
    print("=" * 50)

    registry = ToolCapabilityRegistry()
    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    check(
        "Default capabilities registered",
        all(name in registry.list_tools() for name in [
            "none",
            "filesystem_search",
            "filesystem_edit",
            "memory",
            "terminal",
            "browser",
            "application",
            "system"
        ])
    )

    check(
        "Terminal marked high risk",
        registry.get("terminal")["risk"] == "high"
    )

    check(
        "Terminal requires confirmation",
        registry.get("terminal")["requires_confirmation"] is True
    )

    check(
        "Action lookup works",
        "filesystem_search" in registry.find_by_action("read")
    )

    registry.register(
        "test_tool",
        "A test capability",
        ["test_action"],
        risk="low"
    )

    check(
        "Custom capability registration works",
        registry.get("test_tool")["description"] == "A test capability"
    )

    check(
        "Unknown capability returns None",
        registry.get("missing_tool") is None
    )

    check(
        "Returned metadata cannot mutate registry",
        registry.get("terminal")["actions"].append("unsafe")
        is None
        and "unsafe" not in registry.get("terminal")["actions"]
    )

    try:
        registry.register(
            "bad_tool",
            "Invalid risk",
            [],
            risk="extreme"
        )
        invalid_risk_rejected = False
    except ValueError:
        invalid_risk_rejected = True

    check("Invalid risk level rejected", invalid_risk_rejected)

    print("\n" + "=" * 50)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("TOOL CAPABILITY REGISTRY: PASS")
    else:
        print("TOOL CAPABILITY REGISTRY: FAIL")


if __name__ == "__main__":
    main()
