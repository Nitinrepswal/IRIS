class ConversationLoop:
    def __init__(self, model, max_messages=10):
        self.model = model
        self.max_messages = max_messages
        self.history = []

    def chat(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })

        self._trim_history()

        response = self.model.chat(self.history)

        self.history.append({
            "role": "assistant",
            "content": response
        })

        self._trim_history()

        return response

    def _trim_history(self):
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]

    def clear(self):
        self.history = []

    def get_history(self):
        return self.history