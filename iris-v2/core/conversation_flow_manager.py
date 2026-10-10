
from core.conversation_topic_tracker import ConversationTopicTracker


class ConversationFlowManager:
    def __init__(self):
        self.topic_tracker = ConversationTopicTracker()
        self.last_action = "start"
        self.transitions = []

    def process(self, message):
        if not isinstance(message, str) or not message.strip():
            return {
                "action": "clarify",
                "topic": self.topic_tracker.get_topic(),
                "reason": "Empty or invalid message"
            }

        previous_topic = self.topic_tracker.get_topic()
        result = self.topic_tracker.update(message)

        if result["type"] == "new_topic":
            action = "new_topic"
        elif result["type"] == "follow_up":
            action = "continue_topic"
        else:
            action = "clarify"

        current_topic = self.topic_tracker.get_topic()

        if action == "new_topic":
            self.transitions.append({
                "from": previous_topic,
                "to": current_topic
            })

        self.last_action = action

        return {
            "action": action,
            "topic": current_topic,
            "previous_topic": previous_topic,
            "reason": result.get("reason", "")
        }

    def get_state(self):
        return {
            "current_topic": self.topic_tracker.get_topic(),
            "last_action": self.last_action,
            "transitions": [
                dict(item) for item in self.transitions
            ]
        }

    def export_state(self):
        return {
            "topic_tracker": self.topic_tracker.export_state(),
            "last_action": self.last_action,
            "transitions": [
                dict(item) for item in self.transitions
            ]
        }

    def restore_state(self, data):
        if not isinstance(data, dict):
            raise ValueError("Invalid conversation flow state")

        last_action = data.get("last_action")
        transitions = data.get("transitions")
        tracker_state = data.get("topic_tracker")

        allowed_actions = {
            "start",
            "new_topic",
            "continue_topic",
            "clarify"
        }

        if last_action not in allowed_actions:
            raise ValueError("Invalid last flow action")

        if not isinstance(transitions, list):
            raise ValueError("Flow transitions must be a list")

        validated_transitions = []

        for item in transitions:
            if not isinstance(item, dict):
                raise ValueError("Invalid flow transition")

            source = item.get("from")
            target = item.get("to")

            if not isinstance(source, str) or not isinstance(target, str):
                raise ValueError("Transition topics must be strings")

            validated_transitions.append({
                "from": source,
                "to": target
            })

        tracker_check = ConversationTopicTracker()
        tracker_check.restore_state(tracker_state)

        self.topic_tracker.restore_state(tracker_state)
        self.last_action = last_action
        self.transitions = validated_transitions

    def clear(self):
        self.topic_tracker.clear()
        self.last_action = "start"
        self.transitions.clear()
