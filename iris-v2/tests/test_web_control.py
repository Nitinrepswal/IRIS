from core.web_control import WebControl


def main():
    controller = WebControl()

    print("Searching web...")

    results = controller.execute(
        "search web for Python programming"
    )

    print(results)

    print()
    print("Opening webpage...")

    result = controller.execute(
        "open https://example.com"
    )

    print(result)


if __name__ == "__main__":
    main()