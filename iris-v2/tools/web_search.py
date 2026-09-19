from urllib.parse import quote
from urllib.request import Request, urlopen
import json

from tools.tool import Tool


class WebSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Searches the web and returns search results."
        )

    def execute(self, query, limit=5):
        encoded_query = quote(query)

        url = (
            "https://api.duckduckgo.com/"
            f"?q={encoded_query}"
            "&format=json"
            "&no_html=1"
            "&skip_disambig=1"
        )

        request = Request(
            url,
            headers={
                "User-Agent": "IRIS/1.0"
            }
        )

        with urlopen(request, timeout=10) as response:
            data = json.loads(
                response.read().decode(
                    "utf-8",
                    errors="ignore"
                )
            )

        results = []

        if data.get("AbstractText"):
            results.append({
                "title": data.get("Heading", ""),
                "url": data.get("AbstractURL", ""),
                "snippet": data.get("AbstractText", "")
            })

        for item in data.get("RelatedTopics", []):
            if "Topics" in item:
                for topic in item["Topics"]:
                    if len(results) >= limit:
                        break

                    if "Text" in topic and "FirstURL" in topic:
                        results.append({
                            "title": topic["Text"],
                            "url": topic["FirstURL"],
                            "snippet": topic["Text"]
                        })

            elif "Text" in item and "FirstURL" in item:
                results.append({
                    "title": item["Text"],
                    "url": item["FirstURL"],
                    "snippet": item["Text"]
                })

            if len(results) >= limit:
                break

        return results[:limit]