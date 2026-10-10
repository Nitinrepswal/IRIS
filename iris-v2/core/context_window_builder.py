
class ContextWindowBuilder:
    def __init__(self, retrieval, max_characters=3000):
        if type(max_characters) is not int or max_characters < 1:
            raise ValueError("Character limit must be a positive integer")

        self.retrieval = retrieval
        self.max_characters = max_characters

    def build(self, query, limit=5, topic_aware=True):
        if not isinstance(query, str) or not query.strip():
            return {
                "query": query if isinstance(query, str) else "",
                "topic": "",
                "context": "",
                "messages": [],
                "count": 0,
                "character_count": 0,
                "truncated": False
            }

        result = self.retrieval.retrieve(
            query=query,
            limit=limit,
            topic_aware=topic_aware
        )

        selected = []
        sections = []
        character_count = 0
        truncated = False

        for message in result["messages"]:
            role = message["role"]
            content = message["content"]
            section = f"{role.capitalize()}: {content}"

            separator_length = 2 if sections else 0
            available = self.max_characters - character_count - separator_length

            if available <= 0:
                truncated = True
                break

            if len(section) > available:
                prefix = f"{role.capitalize()}: "
                if available <= len(prefix):
                    truncated = True
                    break

                section = prefix + content[:available - len(prefix)]
                truncated = True

            if sections:
                character_count += 2

            sections.append(section)
            selected.append({
                "role": role,
                "content": section[len(prefix):] if False else (
                    section.split(": ", 1)[1]
                ),
                "score": message.get("score", 0)
            })
            character_count += len(section)

            if truncated:
                break

        return {
            "query": query,
            "topic": result["topic"],
            "context": "\n\n".join(sections),
            "messages": selected,
            "count": len(selected),
            "character_count": character_count,
            "truncated": truncated
        }
