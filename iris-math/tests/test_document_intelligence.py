import os


class DocumentTool:
    def document_exists(self, path):
        return os.path.isfile(path)

    def read_document(self, path):
        if not self.document_exists(path):
            return "Document not found"

        with open(path, "r") as file:
            return file.read()

    def word_count(self, text):
        return len(text.split())


class IRISDocumentAgent:
    def __init__(self):
        self.document = DocumentTool()

    def run(self, path):
        print("IRIS DOCUMENT INTELLIGENCE")
        print("=" * 40)

        print("\nDOCUMENT")
        print(path)

        if not self.document.document_exists(path):
            print("\nDocument not found")
            return

        content = self.document.read_document(path)

        print("\nCONTENT")
        print(content)

        print("\nWORD COUNT")
        print(self.document.word_count(content))


document_path = "/Users/nitin/Desktop/IRIS/iris-math/document.txt"

if not os.path.exists(document_path):
    with open(document_path, "w") as file:
        file.write(
            "IRIS is an intelligent AI assistant. "
            "It can use tools, memory, and reasoning "
            "to help users complete tasks."
        )


agent = IRISDocumentAgent()
agent.run(document_path)