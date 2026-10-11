import json
import os

import ollama
from PIL import Image


class VisionEngine:
    def __init__(self):
        self.model = "granite3.2-vision:2b"
        self.max_size = (256, 160)

    def prepare_image(self, image_path):
        with Image.open(image_path) as image:
            image.load()

            if (
                image.width <= self.max_size[0]
                and image.height <= self.max_size[1]
            ):
                return image_path

            base, extension = os.path.splitext(image_path)
            resized_path = f"{base}_vision{extension}"

            image.thumbnail(self.max_size)
            image.save(resized_path)

            return resized_path

    def analyze(self, image_path, prompt=None):
        if prompt is None:
            prompt = (
                "Analyze this computer screenshot. Return only valid JSON "
                "with keys: application, screen_summary, visible_elements, "
                "suggested_actions. Keep application and screen_summary "
                "brief. Include at most 5 visible elements, each with type "
                "and description strings. Include at most 3 suggested "
                "actions as strings. Do not invent details. Close the JSON "
                "completely."
            )

        prepared_image = self.prepare_image(image_path)

        response = ollama.chat(
            model=self.model,
            options={"num_predict": 400},
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [prepared_image],
                }
            ],
        )

        return response["message"]["content"]

    def understand_screen(self, image_path):
        try:
            raw_result = self.analyze(image_path)
            data = json.loads(raw_result)

            if not isinstance(data, dict):
                raise ValueError("Vision response must be a JSON object")

            application = data.get("application")
            summary = data.get("screen_summary")
            elements = data.get("visible_elements")
            actions = data.get("suggested_actions")

            if not isinstance(application, str) or not application.strip():
                raise ValueError("Invalid application description")

            if not isinstance(summary, str) or not summary.strip():
                raise ValueError("Invalid screen summary")

            if not isinstance(elements, list):
                raise ValueError("visible_elements must be a list")

            for element in elements:
                if not isinstance(element, dict):
                    raise ValueError("Each visible element must be an object")

                if (
                    not isinstance(element.get("type"), str)
                    or not isinstance(element.get("description"), str)
                ):
                    raise ValueError(
                        "Each element requires type and description strings"
                    )

            if not isinstance(actions, list) or not all(
                isinstance(action, str) for action in actions
            ):
                raise ValueError("suggested_actions must be a list of strings")

            return {
                "success": True,
                "application": application.strip(),
                "screen_summary": summary.strip(),
                "visible_elements": elements,
                "suggested_actions": actions,
            }

        except Exception as error:
            return {
                "success": False,
                "message": str(error),
            }

    def detect_ui_elements(self, screen):
        if not isinstance(screen, dict):
            raise ValueError("screen must be a dictionary")

        if not screen.get("success"):
            raise ValueError("Screen understanding was unsuccessful")

        elements = screen.get("visible_elements")

        if not isinstance(elements, list):
            raise ValueError("visible_elements must be a list")

        detected = []

        for element in elements:
            if not isinstance(element, dict):
                raise ValueError("Each UI element must be a dictionary")

            element_type = element.get("type")
            description = element.get("description")

            if not isinstance(element_type, str) or not element_type.strip():
                raise ValueError("Each UI element needs a type")

            if not isinstance(description, str) or not description.strip():
                raise ValueError("Each UI element needs a description")

            element_type = "_".join(
                element_type.strip().lower().replace("-", " ").split()
            )

            bbox = element.get("bbox")

            if bbox is not None:
                if (
                    not isinstance(bbox, (list, tuple))
                    or len(bbox) != 4
                    or any(
                        isinstance(value, bool)
                        or not isinstance(value, (int, float))
                        or value < 0
                        for value in bbox
                    )
                ):
                    raise ValueError(
                        "bbox must contain four non-negative numbers"
                    )

                x1, y1, x2, y2 = bbox

                if x2 < x1 or y2 < y1:
                    raise ValueError("bbox coordinates are invalid")

                bbox = list(bbox)

            detected.append(
                {
                    "type": element_type,
                    "description": description.strip(),
                    "bbox": bbox,
                }
            )

        return detected

    def execute(self, image_path, prompt=None):
        try:
            result = self.analyze(image_path, prompt)
            return {
                "success": True,
                "description": result,
            }
        except Exception as error:
            return {
                "success": False,
                "message": str(error),
            }