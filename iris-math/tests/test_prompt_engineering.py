class PromptBuilder:
    def __init__(self):
        self.system = ""
        self.context = ""
        self.user = ""
        self.output_format = ""

    def set_system(self, instruction):
        self.system = instruction

    def set_context(self, context):
        self.context = context

    def set_user(self, request):
        self.user = request

    def set_output_format(self, output_format):
        self.output_format = output_format

    def build(self):
        prompt = ""

        if self.system:
            prompt += f"SYSTEM:\n{self.system}\n\n"

        if self.context:
            prompt += f"CONTEXT:\n{self.context}\n\n"

        if self.user:
            prompt += f"USER:\n{self.user}\n\n"

        if self.output_format:
            prompt += f"OUTPUT FORMAT:\n{self.output_format}\n"

        return prompt


prompt = PromptBuilder()

prompt.set_system(
    "You are IRIS, a helpful AI programming assistant."
)

prompt.set_context(
    "The user is learning Python and prefers simple explanations."
)

prompt.set_user(
    "Explain what a Python list is."
)

prompt.set_output_format(
    "Give a definition, one example, and one common mistake."
)

final_prompt = prompt.build()

print("Generated prompt:")
print(final_prompt)