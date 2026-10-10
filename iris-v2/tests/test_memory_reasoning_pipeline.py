
from core.memory_reasoning import MemoryReasoning
from core.evidence_conflict_detector import EvidenceConflictDetector


class MemoryReasoningPipeline:
    def __init__(self, conversation):
        self.reasoning = MemoryReasoning(conversation)
        self.conflict_detector = EvidenceConflictDetector()

    def _confidence_score(self, evidence, conflicts):
        if not evidence:
            return 0.0

        scores = []

        for item in evidence:
            score = item.get("score", 0)

            if isinstance(score, bool) or not isinstance(
                score, (int, float)
            ):
                score = 0

            scores.append(max(0.0, min(float(score), 5.0)) / 5.0)

        retrieval_score = sum(scores) / len(scores)
        quantity_score = min(len(evidence) / 3.0, 1.0)

        confidence = retrieval_score * 0.7 + quantity_score * 0.3

        if conflicts:
            confidence *= 0.5

        return round(max(0.0, min(confidence, 1.0)), 3)

    def analyze(self, query, limit=5, min_score=0):
        package = self.reasoning.build_answer_package(
            query=query,
            limit=limit,
            min_score=min_score
        )

        evidence = package["evidence"]
        conflict_result = self.conflict_detector.detect(evidence)
        conflicts = conflict_result["conflicts"]

        if not evidence:
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
            "answer_ready": bool(evidence) and not conflicts,
            "evidence": evidence,
            "sources": package["sources"],
            "evidence_count": package["evidence_count"],
            "conflicts": conflicts,
            "conflict_count": conflict_result["count"],
            "confidence_score": self._confidence_score(
                evidence,
                conflicts
            ),
            "confidence_type": "heuristic",
            "limitations": limitations
        }
