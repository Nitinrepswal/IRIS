
class HumanApproval:
    def request(self, action):
        if not isinstance(action, str) or not action.strip():
            return False

        answer = input(
            f"IRIS wants to perform '{action}'. Approve? (y/n): "
        )

        return answer.strip().lower() == "y"
