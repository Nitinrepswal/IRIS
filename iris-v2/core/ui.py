class IRISUI:
    def show_banner(self):
        print("=" * 40)
        print("            IRIS V2")
        print("      Intelligent AI Assistant")
        print("=" * 40)

    def show_response(self, response):
        print(f"\nIRIS: {response}")

    def show_status(self, message):
        print(f"[IRIS] {message}")

    def show_goodbye(self):
        print("\nIRIS: Goodbye.")