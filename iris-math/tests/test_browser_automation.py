from urllib.request import urlopen
from urllib.error import URLError


class BrowserTool:
    def open_page(self, url):
        try:
            with urlopen(url, timeout=10) as response:
                content = response.read().decode("utf-8")

            return content

        except URLError as error:
            return f"Browser error: {error}"


class IRISBrowserAgent:
    def __init__(self):
        self.browser = BrowserTool()

    def run(self, url):
        print("USER")
        print(f"Open this webpage: {url}")

        print("\nACTION")
        print("open_page")

        content = self.browser.open_page(url)

        print("\nOBSERVATION")

        if content.startswith("Browser error"):
            print(content)
            return

        print(f"Page loaded successfully")
        print(f"Characters received: {len(content)}")

        print("\nPAGE PREVIEW")
        print(content[:300])

        print("\nFINAL ANSWER")
        print("The webpage was opened successfully.")


agent = IRISBrowserAgent()

print("=" * 40)
print("IRIS BROWSER AUTOMATION")
print("=" * 40)

agent.run("https://example.com")