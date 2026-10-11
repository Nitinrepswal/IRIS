
from core.visual_action_planner import VisualActionPlanner


def main():
    planner = VisualActionPlanner()

    elements = [
        {"type": "text_field", "description": "Search field"},
        {"type": "button", "description": "Submit button"},
        {"type": "button", "description": "Cancel button"}
    ]

    result = planner.plan("Find the search field", elements)

    assert result["success"] is True
    assert len(result["steps"]) >= 1
    assert result["steps"][0]["target"]["description"] == "Search field"

    empty_goal = planner.plan("", elements)
    assert empty_goal["success"] is False

    invalid_elements = planner.plan("Find a button", "invalid")
    assert invalid_elements["success"] is False

    no_match = planner.plan("Find a calendar", elements)
    assert no_match["success"] is True
    assert no_match["steps"] == []

    print("VISUAL ACTION PLANNER TEST: PASS")


if __name__ == "__main__":
    main()
