import re

from core.computer_control import ComputerControl
from tools.web_search import WebSearchTool


class WebControl:
    def __init__(self):
        self.computer = ComputerControl()
        self.search_tool = WebSearchTool()

    def search(self, query):
        return self.search_tool.execute(
            query
        )

    def open(self, url):
        return self.computer.open_webpage(
            url
        )

    def launch(self, url):
        return self.computer.launch_webpage(
            url
        )

    def execute(self, message):
        text = message.strip()
        lower = text.lower()

        if lower.startswith("search web for "):
            query = text[15:].strip()

            if not query:
                return None

            results = self.search(query)

            if not results:
                return "No web results found."

            output = []

            for result in results:
                title = result.get("title", "")
                url = result.get("url", "")
                snippet = result.get("snippet", "")

                output.append(
                    f"{title}\n{url}\n{snippet}"
                )

            return "\n\n".join(output)

        match = re.match(
            r"(open|visit|browse)\s+(.+)",
            text,
            re.IGNORECASE
        )

        if match:
            url = match.group(2).strip()

            if not url.startswith(
                ("http://", "https://")
            ):
                url = "https://" + url

            return self.launch(url)["message"]

        return None