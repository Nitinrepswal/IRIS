from tools.web_retriever import WebRetrieverTool


def main():
    tool = WebRetrieverTool()

    print("Tool:", tool.name)
    print("Description:", tool.description)

    result = tool.execute(
        "https://example.com"
    )

    print("\nURL:", result["url"])
    print("Status:", result["status"])
    print("Content:")
    print(result["text"])


if __name__ == "__main__":
    main()