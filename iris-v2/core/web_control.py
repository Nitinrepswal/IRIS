
import re

from core.computer_control import ComputerControl
from tools.web_search import WebSearchTool
from models.llm_model import LLMModel


class WebControl:
    def __init__(self):
        self.computer = ComputerControl()
        self.search_tool = WebSearchTool()
        self.model = LLMModel()

    def search(self, query):
        return self.search_tool.execute(query)

    def open(self, url):
        return self.computer.open_webpage(url)

    def launch(self, url):
        return self.computer.launch_webpage(url)

    def summarize_results(self, query, results):
        sources = []

        for index, result in enumerate(results[:5], start=1):
            sources.append(
                f"Source {index}\n"
                f"Title: {result['title']}\n"
                f"URL: {result['url']}\n"
                f"Content: {result.get('content') or result.get('snippet', '')}"
            )

        source_text = "\n\n".join(sources)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are IRIS, a helpful personal AI assistant. "
                    "Answer the user's search query using only the "
                    "provided web results. Summarize the most relevant "
                    "information in clear, natural language. "
                    "Do not repeat raw snippets. Do not invent facts "
                    "or claim that a source says something it does not. "
                    "If the results do not answer the query, say that "
                    "the available results were insufficient. "
                    "Keep the answer concise, normally 2-5 sentences. "
                    "Do not create source links; the application "
                    "will append the actual links."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Search query: {query}\n\n"
                    f"Web results:\n{source_text}"
                )
            }
        ]

        summary = self.model.chat(messages).strip()

        if not summary:
            summary = "I couldn't create a summary of these results."

        links = "\n".join(
            f"- {result['title']}: {result['url']}"
            for result in results[:3]
        )

        return f"{summary}\n\nSources:\n{links}"
    def execute(self, message):
        text = message.strip()
        lower = text.lower()

        if lower.startswith("search web for "):
            query = text[len("search web for "):].strip()

            if not query:
                return "What would you like me to search for?"

            results = self.search(query)

            if not results:
                return (
                    "I couldn't retrieve web results right now. "
                    "Please try again in a moment."
                )

            return self.summarize_results(query, results)

        match = re.match(
            r"(open|visit|browse)\s+(.+)",
            text,
            re.IGNORECASE
        )

        if match:
            url = match.group(2).strip()

            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            return self.launch(url)["message"]

        return None
