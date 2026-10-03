import os

import ollama
from PIL import Image


class VisionEngine:
    def __init__(self):
        self.model = "granite3.2-vision:2b"
        self.max_size = (256, 160)

    def prepare_image(self, image_path):
        image = Image.open(image_path)

        if image.width <= self.max_size[0] and image.height <= self.max_size[1]:
            return image_path

        base, extension = os.path.splitext(image_path)
        resized_path = f"{base}_ultrafast{extension}"

        image.thumbnail(self.max_size)

        image.save(
            resized_path,
            optimize=True
        )

        return resized_path

    def analyze(self, image_path, prompt=None):
        if prompt is None:
            prompt = (
                "Identify the main app and key UI elements "
                "in one or two short sentences."
            )

        prepared_image = self.prepare_image(image_path)

        response = ollama.chat(
            model=self.model,
            options={
                "num_predict": 24,
                "num_ctx": 2048,
                "temperature": 0
            },
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [prepared_image]
                }
            ]
        )

        return response["message"]["content"]

    def execute(self, image_path, prompt=None):
        try:
            result = self.analyze(
                image_path,
                prompt
            )

            return {
                "success": True,
                "description": result
            }

        except Exception as error:
            return {
                "success": False,
                "message": str(error)
            }