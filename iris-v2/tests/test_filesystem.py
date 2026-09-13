from tools.filesystem import FilesystemSearchTool


def main():
    tool = FilesystemSearchTool()

    print("Tool:", tool.name)
    print("Description:", tool.description)

    results = tool.execute(
        directory=".",
        query="test"
    )

    print("\nMatching files:")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()