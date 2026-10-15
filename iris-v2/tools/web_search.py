
from ddgs import DDGS

from tools.tool import Tool


class WebSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Searches the web and retrieves page content."
        )

    def execute(self, query, limit=5):
        query = query.strip()

        if not query:
            return []

        if query.lower() == "ml":
            query = "machine learning ML"

        try:
            with DDGS() as search:
                results = search.text(
                    query,
                    max_results=limit
                )

                cleaned_results = []

                for result in results or []:
                    title = result.get("title", "").strip()
                    url = result.get("href", "").strip()
                    snippet = result.get("body", "").strip()

                    if not title or not url:
                        continue

                    content = ""

                    if len(cleaned_results) < 3:
                        try:
                            page = search.extract(
                                url,
                                fmt="text_plain"
                            )
                            content = page.get("content", "").strip()
                        except Exception as error:
                            print(
                                f"[IRIS] Could not extract {url}: "
                                f"{error}"
                            )

                    cleaned_results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet,
                        "content": content[:5000]
                    })

                return cleaned_results

        except Exception as error:
            print(f"[IRIS] Web search error: {error}")
            return []
