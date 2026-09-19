from urllib.request import Request, urlopen
from html.parser import HTMLParser

from tools.tool import Tool


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {
            "style",
            "script",
            "noscript"
        }
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth > 0:
            return

        text = data.strip()

        if text:
            self.text.append(text)

    def get_text(self):
        return " ".join(self.text)


class BrowserTool(Tool):
    def __init__(self):
        super().__init__(
            name="browser",
            description="Fetches and extracts text from a webpage."
        )

    def execute(self, url):
        request = Request(
            url,
            headers={
                "User-Agent": "IRIS/1.0"
            }
        )

        with urlopen(request, timeout=10) as response:
            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            if "text/html" not in content_type:
                return {
                    "url": url,
                    "status": response.status,
                    "text": ""
                }

            html = response.read().decode(
                "utf-8",
                errors="ignore"
            )

        parser = TextExtractor()
        parser.feed(html)

        return {
            "url": url,
            "status": 200,
            "text": parser.get_text()
        }