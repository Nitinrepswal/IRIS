
from core.memory_reasoning import MemoryReasoning
from core.evidence_conflict_detector import EvidenceConflictDetector


class MemoryReasoningPipeline:
    def __init__(self, conversation):
        self.reasoning = MemoryReasoning(conversation)
        self.conflict_detector = EvidenceConflictDetector()

    def analyze(self, query, limit=5, min_score=0):
        package = self.reasoning.build_answer_package(
            query=query,
            limit=limit,
            min_score=min_score
        )

        conflict_result = self.conflict_detector.detect(
            package["evidence"]
        )

        conflicts = conflict_result["conflicts"]

        if not package["evidence"]:
            status = "insufficient_evidence"
        elif conflicts:
            status = "potential_conflict"
        else:
            status = "evidence_found"

        limitations = list(package["limitations"])

        if conflicts:
            limitations.append(
                "Retrieved evidence contains potential conflicts."
            )

        return {
            "query": package["query"],
            "status": status,
            "answer_ready": (
                bool(package["evidence"]) and not conflicts
            ),
            "evidence": package["evidence"],
            "sources": package["sources"],
            "evidence_count": package["evidence_count"],
            "conflicts": conflicts,
            "conflict_count": conflict_result["count"],
            "limitations": limitations
        }
