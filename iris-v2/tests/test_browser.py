from tools.browser import BrowserTool


def main():
    browser = BrowserTool()

    print("Tool:", browser.name)
    print("Description:", browser.description)

    result = browser.execute(
        "https://example.com"
    )

    print("\nURL:", result["url"])
    print("Status:", result["status"])
    print("Content:")
    print(result["text"])


if __name__ == "__main__":
    main()