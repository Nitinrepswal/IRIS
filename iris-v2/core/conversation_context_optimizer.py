
class ConversationContextOptimizer:
    def __init__(self, max_characters=3000):
        if type(max_characters) is not int or max_characters < 1:
            raise ValueError("Character limit must be a positive integer")

        self.max_characters = max_characters

    def optimize(self, messages):
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")

        candidates = []
        seen = set()

        for index, message in enumerate(messages):
            if not isinstance(message, dict):
                continue

            role = message.get("role")
            content = message.get("content")

            if role not in ("user", "assistant"):
                continue

            if not isinstance(content, str) or not content.strip():
                continue

            normalized = " ".join(content.lower().split())

            if normalized in seen:
                continue

            seen.add(normalized)

            score = message.get("topic_score", 0) + message.get("score", 0)

            if type(score) not in (int, float) or score < 0:
                score = 0

            section = f"{role.capitalize()}: {content.strip()}"

            candidates.append({
                "role": role,
                "content": content.strip(),
                "score": score,
                "section": section,
                "index": index
            })

        candidates.sort(
            key=lambda item: (
                item["score"] / max(len(item["section"]), 1),
                item["score"],
                -item["index"]
            ),
            reverse=True
        )

        selected = []
        sections = []
        character_count = 0
        truncated = False

        for item in candidates:
            separator_length = 2 if sections else 0
            available = (
                self.max_characters
                - character_count
                - separator_length
            )

            if available <= 0:
                truncated = True
                break

            section = item["section"]

            if len(section) > available:
                prefix = f"{item['role'].capitalize()}: "

                if available <= len(prefix):
                    truncated = True
                    continue

                content = item["content"][
                    :available - len(prefix)
                ]

                section = prefix + content
                truncated = True
            else:
                content = item["content"]

            if sections:
                character_count += 2

            sections.append(section)
            character_count += len(section)

            selected.append({
                "role": item["role"],
                "content": content,
                "score": item["score"]
            })

            if truncated:
                break

        context = "\n\n".join(sections)

        return {
            "context": context,
            "messages": selected,
            "count": len(selected),
            "character_count": len(context),
            "truncated": truncated
        }
