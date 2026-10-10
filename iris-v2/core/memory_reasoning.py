
import hashlib
import json
import math
import time
from pathlib import Path


class MemoryReasoning:
    IMPORTANCE_PATTERNS = {
        "identity": ("my name is", "i am ", "i'm "),
        "preferences": (
            "i prefer", "i like", "i dislike",
            "i want", "i don't like"
        ),
        "commitments": (
            "my goal is", "i plan to", "remember that",
            "i decided to", "i will"
        ),
        "projects": (
            "my project", "i am building",
            "i'm building", "working on"
        )
    }

    EPISODIC_PATTERNS = (
        "yesterday", "last week", "last month", "last year",
        "today i", "i attended", "i visited", "i went",
        "i experienced", "i completed", "i finished",
        "i met", "i tried"
    )

    SEMANTIC_PATTERNS = (
        " is a ", " are ", " refers to ", " means ",
        " is used for ", " is known as ", " is defined as "
    )

    VALID_MEMORY_TYPES = {"episodic", "semantic"}

    IMPORTANCE_FEEDBACK_VALUES = {
        "important": 1.0,
        "neutral": 0.0,
        "unimportant": -1.0
    }

    MEMORY_PRIVACY_VALUES = {"normal", "private", "excluded"}

    def __init__(self, conversation):
        self.conversation = conversation
        self._importance_feedback = {}
        self._memory_privacy = {}

    def set_memory_privacy(self, memory_id, privacy):
        if not isinstance(memory_id, str) or not memory_id.strip():
            raise ValueError("memory_id must be a non-empty string")

        if (
            not isinstance(privacy, str)
            or privacy not in self.MEMORY_PRIVACY_VALUES
        ):
            raise ValueError(
                "privacy must be 'normal', 'private', or 'excluded'"
            )

        self._memory_privacy[memory_id] = privacy
        return {"memory_id": memory_id, "privacy": privacy}

    def get_memory_privacy(self, memory_id):
        return self._memory_privacy.get(memory_id, "normal")

    def save_memory_privacy(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_name(path.name + ".tmp")

        try:
            temp_path.write_text(
                json.dumps(self._memory_privacy, indent=2),
                encoding="utf-8"
            )
            temp_path.replace(path)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def load_memory_privacy(self, path):
        path = Path(path)

        if not path.exists():
            self._memory_privacy = {}
            return

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid memory privacy file") from exc

        if not isinstance(data, dict):
            raise ValueError("Memory privacy must be a JSON object")

        for memory_id, privacy in data.items():
            if not isinstance(memory_id, str) or not memory_id.strip():
                raise ValueError("Invalid memory ID in privacy file")

            if (
                not isinstance(privacy, str)
                or privacy not in self.MEMORY_PRIVACY_VALUES
            ):
                raise ValueError(
                    f"Invalid privacy setting for {memory_id}"
                )

        self._memory_privacy = dict(data)

    def set_importance_feedback(self, memory_id, feedback):
        if not isinstance(memory_id, str) or not memory_id.strip():
            raise ValueError("memory_id must be a non-empty string")

        if feedback not in self.IMPORTANCE_FEEDBACK_VALUES:
            raise ValueError(
                "feedback must be 'important', 'neutral', or 'unimportant'"
            )

        self._importance_feedback[memory_id] = feedback

        return {
            "memory_id": memory_id,
            "importance_feedback": feedback
        }

    def get_importance_feedback(self, memory_id):
        return self._importance_feedback.get(memory_id, "neutral")

    def save_importance_feedback(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = dict(self._importance_feedback)
        temp_path = path.with_name(path.name + ".tmp")

        try:
            temp_path.write_text(
                json.dumps(data, indent=2),
                encoding="utf-8"
            )
            temp_path.replace(path)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def load_importance_feedback(self, path):
        path = Path(path)

        if not path.exists():
            self._importance_feedback = {}
            return

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(
                "Invalid importance feedback file"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                "Importance feedback must be a JSON object"
            )

        for memory_id, feedback in data.items():
            if not isinstance(memory_id, str) or not memory_id.strip():
                raise ValueError(
                    "Invalid memory ID in feedback file"
                )

            if (
                not isinstance(feedback, str)
                or feedback not in self.IMPORTANCE_FEEDBACK_VALUES
            ):
                raise ValueError(
                    f"Invalid importance feedback for {memory_id}"
                )

        self._importance_feedback = dict(data)

    def _stable_memory_id(self, role, content):
        value = f"{role}\0{content}".encode("utf-8")
        digest = hashlib.sha256(value).hexdigest()
        return f"mem_{digest[:24]}"

    def _recency_score(self, timestamp, now):
        if (
            isinstance(timestamp, bool)
            or not isinstance(timestamp, (int, float))
            or not math.isfinite(timestamp)
            or timestamp < 0
            or timestamp > now
        ):
            return 0.0

        age_days = (now - timestamp) / 86400
        return 0.5 ** (age_days / 30)

    def _importance_score(self, role, content):
        text = content.lower()
        score = 0.1
        reasons = []

        if role == "user":
            score += 0.1
            reasons.append("user_message")

        for category, patterns in self.IMPORTANCE_PATTERNS.items():
            if any(pattern in text for pattern in patterns):
                score += 0.2
                reasons.append(category)

        if "important" in text or "remember" in text:
            score += 0.1
            reasons.append("explicit_importance")

        return {
            "score": round(min(score, 1.0), 4),
            "reasons": reasons
        }

    def _classify_memory_type(self, content):
        text = content.lower()

        if any(pattern in text for pattern in self.EPISODIC_PATTERNS):
            return "episodic"

        if any(pattern in text for pattern in self.SEMANTIC_PATTERNS):
            return "semantic"

        return "semantic"

    def _search(self, query, limit):
        if callable(getattr(self.conversation, "search_history", None)):
            return self.conversation.search_history(
                query=query,
                limit=limit,
                topic_aware=False
            )

        search = getattr(self.conversation, "search", None)

        if callable(search):
            return search(
                query=query,
                limit=limit,
                topic_aware=False
            )

        raise TypeError(
            "Conversation must provide search_history() or search()."
        )

    def retrieve_evidence(
        self,
        query,
        limit=5,
        min_score=0,
        deduplicate=True,
        memory_type=None
    ):
        if not isinstance(query, str) or not query.strip():
            return {"query": "", "memories": [], "count": 0}

        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError("limit must be a positive integer")

        if (
            isinstance(min_score, bool)
            or not isinstance(min_score, (int, float))
            or not math.isfinite(min_score)
            or min_score < 0
        ):
            raise ValueError("min_score must be a non-negative number")

        if not isinstance(deduplicate, bool):
            raise ValueError("deduplicate must be a boolean")

        if memory_type is not None and (
            not isinstance(memory_type, str)
            or memory_type not in self.VALID_MEMORY_TYPES
        ):
            raise ValueError(
                "memory_type must be 'episodic', 'semantic', or None"
            )

        candidate_limit = max(limit * 10, 50)
        results = self._search(query.strip(), candidate_limit)

        now = time.time()
        memories = []
        seen_ids = set()

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
                or not math.isfinite(score)
            ):
                score = 0

            if score < min_score:
                continue

            classified_type = self._classify_memory_type(content)

            if memory_type is not None and classified_type != memory_type:
                continue

            memory_id = self._stable_memory_id(role, content)
            privacy = self.get_memory_privacy(memory_id)

            if privacy in ("private", "excluded"):
                continue

            if deduplicate and memory_id in seen_ids:
                continue

            seen_ids.add(memory_id)

            timestamp = result.get("timestamp")
            recency = self._recency_score(timestamp, now)
            importance = self._importance_score(role, content)

            retrieval_score = max(0.0, min(float(score), 5.0))

            importance_feedback = self.get_importance_feedback(memory_id)
            feedback_adjustment = (
                0.25
                * self.IMPORTANCE_FEEDBACK_VALUES[importance_feedback]
            )

            ranking_score = max(
                0.0,
                retrieval_score
                + 0.5 * recency
                + 0.5 * importance["score"]
                + feedback_adjustment
            )

            memories.append({
                "memory_id": memory_id,
                "role": role,
                "content": content,
                "memory_type": classified_type,
                "score": score,
                "timestamp": timestamp,
                "recency_score": round(recency, 4),
                "importance_score": importance["score"],
                "importance_reasons": importance["reasons"],
                "importance_feedback": importance_feedback,
                "feedback_adjustment": round(feedback_adjustment, 4),
                "privacy": privacy,
                "ranking_score": round(ranking_score, 4),
                "source_index": index,
                "source": {
                    "type": "conversation_search_result",
                    "memory_id": memory_id,
                    "result_index": index,
                    "role": role
                }
            })

        memories.sort(
            key=lambda item: (
                -item["ranking_score"],
                item["source_index"]
            )
        )

        memories = memories[:limit]

        return {
            "query": query.strip(),
            "memories": memories,
            "count": len(memories)
        }

    def build_answer_package(
        self,
        query,
        limit=5,
        min_score=0,
        memory_type=None
    ):
        evidence = self.retrieve_evidence(
            query=query,
            limit=limit,
            min_score=min_score,
            memory_type=memory_type
        )

        memories = evidence["memories"]
        enough_evidence = bool(memories)

        sources = [
            {
                "memory_id": memory["memory_id"],
                "source_index": memory["source_index"],
                "role": memory["role"],
                "score": memory["score"],
                "timestamp": memory["timestamp"],
                "source": dict(memory["source"])
            }
            for memory in memories
        ]

        return {
            "query": evidence["query"],
            "evidence": memories,
            "sources": sources,
            "evidence_count": len(memories),
            "status": (
                "evidence_found"
                if enough_evidence
                else "insufficient_evidence"
            ),
            "answer_ready": enough_evidence,
            "limitations": (
                []
                if enough_evidence
                else ["No matching evidence met the retrieval criteria."]
            )
        }
