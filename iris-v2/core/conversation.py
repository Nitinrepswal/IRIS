class ConversationLoop:
    def __init__(self, model):
        self.model = model
        self.history = []

    def chat(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })

        response = self.model.chat(self.history)

        self.history.append({
            "role": "assistant",
            "content": response
        })

        return response