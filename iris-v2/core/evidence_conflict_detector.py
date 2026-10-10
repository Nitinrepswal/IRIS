
import re


class EvidenceConflictDetector:
    def __init__(self):
        self.patterns = [
            re.compile(
                r"\b(?:uses?|using|built with|powered by)\s+"
                r"([a-z][a-z0-9+#.-]*)",
                re.IGNORECASE
            ),
            re.compile(
                r"\b(?:database|db)\s+(?:is|uses?)\s+"
                r"([a-z][a-z0-9+#.-]*)",
                re.IGNORECASE
            )
        ]

    def _extract_fact(self, content):
        if not isinstance(content, str):
            return None

        for pattern in self.patterns:
            match = pattern.search(content)

            if match:
                value = match.group(1).lower().rstrip(".,;:!?")

                return {
                    "type": "technology",
                    "value": value
                }

        return None

    def detect(self, memories):
        if not isinstance(memories, list):
            raise ValueError("memories must be a list")

        facts = []

        for index, memory in enumerate(memories):
            if not isinstance(memory, dict):
                continue

            content = memory.get("content")
            fact = self._extract_fact(content)

            if fact is None:
                continue

            facts.append({
                "memory_index": index,
                "content": content,
                "fact_type": fact["type"],
                "value": fact["value"]
            })

        conflicts = []

        for index, first in enumerate(facts):
            for second in facts[index + 1:]:
                if (
                    first["fact_type"] == second["fact_type"]
                    and first["value"] != second["value"]
                ):
                    conflicts.append({
                        "type": first["fact_type"],
                        "values": sorted([
                            first["value"],
                            second["value"]
                        ]),
                        "evidence": [
                            {
                                "memory_index": first["memory_index"],
                                "content": first["content"]
                            },
                            {
                                "memory_index": second["memory_index"],
                                "content": second["content"]
                            }
                        ],
                        "status": "potential_conflict"
                    })

        return {
            "conflicts": conflicts,
            "count": len(conflicts)
        }
