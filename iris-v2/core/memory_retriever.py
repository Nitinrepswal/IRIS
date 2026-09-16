import math


class MemoryRetriever:
    def __init__(self, model, memories):
        self.model = model
        self.memories = memories
        self.embeddings = []

        self._build_embeddings()

    def _embed(self, text):
        result = self.model.embed(text)

        return result["embeddings"][0]

    def _build_embeddings(self):
        self.embeddings = []

        for memory in self.memories:
            embedding = self._embed(memory)
            self.embeddings.append(embedding)

    def _similarity(self, vector_a, vector_b):
        dot_product = sum(
            a * b for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = math.sqrt(
            sum(a * a for a in vector_a)
        )

        magnitude_b = math.sqrt(
            sum(b * b for b in vector_b)
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0

        return dot_product / (magnitude_a * magnitude_b)

    def retrieve(self, query, top_k=3, threshold=0.5):
        query_embedding = self._embed(query)

        results = []

        for memory, embedding in zip(
            self.memories,
            self.embeddings
        ):
            score = self._similarity(
                query_embedding,
                embedding
            )

            if score >= threshold:
                results.append({
                    "memory": memory,
                    "score": score
                })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:top_k]