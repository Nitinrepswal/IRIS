
class MemoryReasoning:
    def __init__(self, conversation):
        self.conversation = conversation

    def retrieve_evidence(self, query, limit=5, min_score=0):
        if not isinstance(query, str) or not query.strip():
            return {
                "query": "",
                "memories": [],
                "count": 0
            }

        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError("limit must be a positive integer")

        if (
            isinstance(min_score, bool)
            or not isinstance(min_score, (int, float))
            or min_score < 0
        ):
            raise ValueError("min_score must be a non-negative number")

        results = self.conversation.search(
            query=query,
            limit=limit * 3,
            topic_aware=False
        )

        memories = []

        for index, result in enumerate(results):
            if not isinstance(result, dict):
                continue

            role = result.get("role")
            content = result.get("content")
            score = result.get("score", 0)

            if role not in ("user", "assistant"):
                continue

            if not isinstance(content, str) or not content.strip():
                continue

            if (
                isinstance(score, bool)
                or not isinstance(score, (int, float))
            ):
                score = 0

            if score < min_score:
                continue

            memories.append({
                "role": role,
                "content": content,
                "score": score,
                "source_index": index
            })

        memories.sort(
            key=lambda item: (-item["score"], item["source_index"])
        )

        memories = memories[:limit]

        return {
            "query": query.strip(),
            "memories": memories,
            "count": len(memories)
        }

    def build_answer_package(self, query, limit=5, min_score=0):
        evidence = self.retrieve_evidence(
            query=query,
            limit=limit,
            min_score=min_score
        )

        memories = evidence["memories"]
        enough_evidence = len(memories) > 0

        sources = [
            {
                "source_index": memory["source_index"],
                "role": memory["role"],
                "score": memory["score"]
            }
            for memory in memories
        ]

        return {
            "query": evidence["query"],
            "evidence": memories,
            "sources": sources,
            "evidence_count": len(memories),
            "status": "evidence_found" if enough_evidence else "insufficient_evidence",
            "answer_ready": enough_evidence,
            "limitations": (
                []
                if enough_evidence
                else ["No matching evidence met the retrieval criteria."]
            )
        }
