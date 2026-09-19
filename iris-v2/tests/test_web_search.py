from tools.web_search import WebSearchTool


def main():
    tool = WebSearchTool()

    print("Tool:", tool.name)
    print("Description:", tool.description)

    results = tool.execute(
        "Python programming language",
        limit=5
    )

    print("\nSearch results:")

    for index, result in enumerate(results, start=1):
        print(f"\n{index}. {result['title']}")
        print("URL:", result["url"])
        print("Snippet:", result["snippet"])


if __name__ == "__main__":
    main()