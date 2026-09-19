from tools.tool import Tool
from tools.browser import BrowserTool


class WebRetrieverTool(Tool):
    def __init__(self):
        super().__init__(
            name="web_retriever",
            description="Retrieves readable text from a webpage."
        )

        self.browser = BrowserTool()

    def execute(self, url):
        return self.browser.execute(url)