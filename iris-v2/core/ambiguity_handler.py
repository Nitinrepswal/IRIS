
class AmbiguityHandler:
    VAGUE_PHRASES = {
        "do it",
        "fix it",
        "change it",
        "make it better",
        "open it",
        "run it",
        "delete it",
        "that thing",
        "something",
        "do something",
        "help me with this"
    }

    def __init__(self):
        self.last_request = None

    def analyze(self, message, candidates=None):
        if not isinstance(message, str) or not message.strip():
            return self._result(
                False,
                True,
                "Please tell me what you'd like me to do.",
                "empty_request"
            )

        normalized = " ".join(message.lower().strip().split())

        if candidates is not None:
            if (
                not isinstance(candidates, list)
                or not all(
                    isinstance(candidate, str) and candidate.strip()
                    for candidate in candidates
                )
            ):
                return self._result(
                    False,
                    True,
                    "Candidate interpretations must be a list of non-empty strings.",
                    "invalid_candidates"
                )

            candidates = list(dict.fromkeys(
                candidate.strip() for candidate in candidates
            ))

            if len(candidates) > 1:
                return self._result(
                    True,
                    True,
                    "I see multiple possible interpretations. Which one do you mean?",
                    "multiple_interpretations",
                    candidates
                )

        if normalized in self.VAGUE_PHRASES:
            return self._result(
                True,
                True,
                "Could you clarify what you'd like me to do?",
                "vague_request"
            )

        if normalized in {"it", "this", "that", "do this", "fix this"}:
            if self.last_request is None:
                return self._result(
                    True,
                    True,
                    "What does 'this' refer to?",
                    "missing_context"
                )

        self.last_request = message.strip()

        return self._result(
            True,
            False,
            "The request appears clear enough to continue.",
            "clear_request"
        )

    def _result(
        self,
        valid,
        needs_clarification,
        question,
        reason,
        candidates=None
    ):
        return {
            "valid": valid,
            "needs_clarification": needs_clarification,
            "question": question,
            "reason": reason,
            "candidates": candidates or []
        }
