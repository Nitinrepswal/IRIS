from models.llm_model import LLMModel
from tools.web_search import WebSearchTool
from tools.web_retriever import WebRetrieverTool


class WebKnowledge:
    def __init__(self):
        self.model = LLMModel()
        self.search_tool = WebSearchTool()
        self.retriever = WebRetrieverTool()

    def search(self, query, limit=3):
        return self.search_tool.execute(
            query,
            limit=limit
        )

    def retrieve(self, results):
        documents = []

        for result in results:
            url = result.get("url", "")

            if not url:
                continue

            try:
                page = self.retriever.execute(url)

                if page.get("status") == 200:
                    text = page.get("text", "")

                    if text:
                        documents.append({
                            "title": result.get("title", ""),
                            "url": url,
                            "text": text[:4000]
                        })

            except Exception:
                continue

        return documents

    def answer(self, question):
        results = self.search(question)

        if not results:
            return "I could not find useful web results."

        documents = self.retrieve(results)

        if not documents:
            return "I found web results, but could not retrieve their content."

        context_parts = []

        for document in documents:
            context_parts.append(
                f"Title: {document['title']}\n"
                f"URL: {document['url']}\n"
                f"Content:\n{document['text']}"
            )

        context = "\n\n---\n\n".join(context_parts)

        prompt = f"""
Answer the user's question using the web knowledge below.

Rules:
- Use the retrieved information as the main source.
- Do not invent facts.
- If the information is insufficient, say so.
- Keep the answer clear and concise.
- Mention relevant sources when useful.

Web knowledge:

{context}

User question:
{question}
"""

        return self.model.chat([
            {
                "role": "user",
                "content": prompt
            }
        ])

    def execute(self, question):
        try:
            response = self.answer(question)

            return {
                "success": True,
                "answer": response
            }

        except Exception as error:
            return {
                "success": False,
                "message": str(error)
            }