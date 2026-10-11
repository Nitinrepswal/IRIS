from core.visual_action_planner import VisualActionPlanner


def main():
    planner = VisualActionPlanner()

    elements = [
        {"type": "button", "description": "Search"},
        {"type": "text_field", "description": ""},
        {"type": "button", "description": "Submit"}
    ]

    result = planner.plan("Find search", elements)
    assert result["success"] is True
    assert len(result["steps"]) == 1
    assert result["steps"][0]["target"]["description"] == "Search"

    result = planner.plan("Find the", elements)
    assert result["success"] is True
    assert result["steps"] == []

    result = planner.plan("Find search", [{"type": "button"}])
    assert result["success"] is False

    result = planner.plan("Find search", [None])
    assert result["success"] is False

    print("DAY 293 VISUAL ACTION PLANNER EDGE TEST: PASS")


if __name__ == "__main__":
    main()