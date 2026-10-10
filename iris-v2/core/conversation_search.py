
import re


class ConversationSearch:
    def _tokenize(self, text):
        return re.findall(r"\b\w+\b", text.lower())

    def search(self, query, messages, limit=5):
        if not isinstance(query, str) or not query.strip():
            return []

        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")

        if type(limit) is not int or limit < 1:
            raise ValueError("Limit must be a positive integer")

        query_words = set(self._tokenize(query))

        if not query_words:
            return []

        normalized_query = " ".join(self._tokenize(query))
        results = []

        for index, message in enumerate(messages):
            if not isinstance(message, dict):
                continue

            role = message.get("role")
            content = message.get("content")

            if role not in ("user", "assistant"):
                continue

            if not isinstance(content, str):
                continue

            message_words = set(self._tokenize(content))
            matched_words = query_words & message_words

            if not matched_words:
                continue

            normalized_content = " ".join(self._tokenize(content))
            phrase_match = normalized_query in normalized_content

            result = {
                "role": role,
                "content": content,
                "score": len(matched_words),
                "phrase_match": phrase_match,
                "index": index
            }

            if message.get("timestamp") is not None:
                result["timestamp"] = message["timestamp"]

            results.append(result)

        results.sort(
            key=lambda item: (
                item["phrase_match"],
                item["score"],
                item["index"]
            ),
            reverse=True
        )

        return [
            {
                "role": result["role"],
                "content": result["content"],
                "score": result["score"],
                "phrase_match": result["phrase_match"],
                **(
                    {"timestamp": result["timestamp"]}
                    if "timestamp" in result
                    else {}
                )
            }
            for result in results[:limit]
        ]
