from core.conversation import ConversationLoop
from core.nlu import NaturalLanguageUnderstanding
from core.intent import IntentDetector
from core.tool_selector import ToolSelector


class IRISBrain:
    def __init__(self, model):
        self.model = model

        self.conversation = ConversationLoop(model)
        self.nlu = NaturalLanguageUnderstanding(model)
        self.intent = IntentDetector(model)
        self.tool_selector = ToolSelector(model)

    def process(self, message):
        understanding = self.nlu.understand(message)

        intent_result = self.intent.detect(message)
        intent = intent_result["intent"]

        tool_result = self.tool_selector.select(
            message,
            intent
        )

        response = self.conversation.chat(message)

        return {
            "understanding": understanding,
            "intent": intent,
            "tool": tool_result["tool"],
            "response": response
        }