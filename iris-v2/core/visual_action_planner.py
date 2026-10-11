
class VisualActionPlanner:
    def plan(self, goal, visible_elements):
        if not isinstance(goal, str) or not goal.strip():
            return {"success": False, "message": "Invalid goal"}

        if not isinstance(visible_elements, list):
            return {"success": False, "message": "Invalid visible elements"}

        for element in visible_elements:
            if not isinstance(element, dict):
                return {"success": False, "message": "Invalid UI element"}

            if (
                not isinstance(element.get("type"), str)
                or not isinstance(element.get("description"), str)
            ):
                return {"success": False, "message": "Invalid UI element"}

        goal_words = set(goal.lower().split())
        ignored_words = {"find", "the", "a", "an", "to", "in", "on", "for"}
        goal_words -= ignored_words

        matches = []

        for element in visible_elements:
            description = element["description"].strip()
            element_type = element["type"].strip()

            if not description or not element_type:
                continue

            text_words = set(
                f"{description} {element_type}".lower().replace("_", " ").split()
            )
            score = len(goal_words & text_words)

            if score:
                matches.append({
                    "target": element,
                    "score": score
                })

        matches.sort(key=lambda item: item["score"], reverse=True)

        return {
            "success": True,
            "goal": goal.strip(),
            "steps": [
                {
                    "step": index + 1,
                    "action": "inspect",
                    "target": match["target"]
                }
                for index, match in enumerate(matches)
            ],
            "message": (
                "Matching elements found"
                if matches
                else "No matching UI elements found"
            )
        }
