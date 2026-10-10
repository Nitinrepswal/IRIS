
from core.intent import IntentDetector
from core.tool_selector import ToolSelector
from core.multi_tool_router import MultiToolRouter
from core.tool_arguments import ToolArgumentGenerator
from core.clarification_engine import ClarificationEngine
from core.tool_dependencies import ToolDependencyDetector
from core.tool_chain import ToolChainPlanner
from core.ambiguity_handler import AmbiguityHandler
from core.tool_confidence import ToolConfidenceScorer
from core.missing_arguments import MissingArgumentDetector


class IntelligenceRouter:
    ARGUMENT_TOOLS = {
        "filesystem_search": "filesystem_search",
        "filesystem_edit": "file_editor",
        "file_reader": "file_reader",
        "terminal": "terminal",
    }

    def __init__(self, model, confidence_threshold=0.60):
        self.model = model
        self.intent_detector = IntentDetector(model)
        self.tool_selector = ToolSelector(model)
        self.multi_tool_router = MultiToolRouter(model)
        self.argument_generator = ToolArgumentGenerator(model)
        self.clarification_engine = ClarificationEngine()
        self.dependency_detector = ToolDependencyDetector()
        self.chain_planner = ToolChainPlanner()
        self.ambiguity_handler = AmbiguityHandler()
        self.confidence_scorer = ToolConfidenceScorer(
            threshold=confidence_threshold
        )
        self.missing_argument_detector = MissingArgumentDetector()

    def route(self, message):
        if not isinstance(message, str) or not message.strip():
            return self._result(
                False, message, "Request must not be empty."
            )

        ambiguity = self.ambiguity_handler.analyze(message)

        if not ambiguity["valid"] or ambiguity["needs_clarification"]:
            return self._result(
                ambiguity["valid"],
                message,
                ambiguity["reason"],
                needs_clarification=ambiguity["needs_clarification"],
                question=ambiguity["question"],
                ambiguity=ambiguity,
            )

        intent_result = self.intent_detector.detect(message)
        intent = intent_result.get("intent")

        if intent not in IntentDetector.ALLOWED_INTENTS:
            return self._result(
                False,
                message,
                "Intent detection returned an unsupported intent.",
                intent=intent,
            )

        tool_result = self.tool_selector.select(message, intent)
        selected_tool = tool_result.get("tool")
        scores = tool_result.get("scores")

        if not isinstance(selected_tool, str):
            return self._result(
                False, message, "Tool selection returned an invalid tool.",
                intent=intent,
            )

        confidence = self.confidence_scorer.score(
            selected_tool, scores
        )

        if not confidence["valid"]:
            return self._result(
                False,
                message,
                confidence["reason"],
                intent=intent,
                tool=selected_tool,
            )

        # Conversation does not require tool-confidence gating.
        if selected_tool == "none":
            return self._result(
                True,
                message,
                "No tool is required; this is a conversational plan.",
                intent=intent,
                tool="none",
                confidence=confidence,
            )

        if not confidence["confident"]:
            return self._result(
                True,
                message,
                "Tool selection confidence is below the threshold.",
                intent=intent,
                tool=selected_tool,
                confidence=confidence,
                needs_clarification=True,
                question=(
                    "I'm not confident about the best action. "
                    "Could you clarify what you'd like me to do?"
                ),
            )

        multi_plan = self.multi_tool_router.route(message)

        if multi_plan.get("needs_clarification"):
            return self._result(
                True,
                message,
                multi_plan.get("reason", "Clarification is required."),
                intent=intent,
                tool=selected_tool,
                confidence=confidence,
                needs_clarification=True,
                question=multi_plan.get("question", ""),
            )

        if not multi_plan.get("valid"):
            return self._result(
                False,
                message,
                multi_plan.get("reason", "Invalid tool plan."),
                intent=intent,
                tool=selected_tool,
                confidence=confidence,
            )

        tasks = multi_plan["steps"]

        # Reject a plan whose first action conflicts with tool selection.
        if tasks[0]["tool"] != selected_tool:
            return self._result(
                False,
                message,
                "Selected tool does not match the first planned step.",
                intent=intent,
                tool=selected_tool,
                confidence=confidence,
            )

        dependency_result = self.dependency_detector.detect(tasks)

        if not dependency_result["valid"]:
            return self._result(
                False,
                message,
                dependency_result["reason"],
                intent=intent,
                tool=selected_tool,
                confidence=confidence,
            )

        chain_result = self.chain_planner.build(
            tasks, dependency_result["dependencies"]
        )

        if not chain_result["valid"]:
            return self._result(
                False,
                message,
                chain_result["reason"],
                intent=intent,
                tool=selected_tool,
                confidence=confidence,
            )

        planned_steps = chain_result["chain"]

        # Extract arguments independently for every supported step.
        for step in planned_steps:
            argument_tool = self.ARGUMENT_TOOLS.get(step["tool"])

            if argument_tool is None:
                continue

            argument_result = self.argument_generator.generate(
                message, argument_tool
            )

            arguments = argument_result.get("arguments", {})

            missing_result = self.missing_argument_detector.detect(
                argument_tool, arguments
            )

            if not missing_result["valid"]:
                missing = missing_result.get("missing", [])

                if missing:
                    clarification = self.clarification_engine.generate(
                        missing
                    )

                    return self._result(
                        clarification["valid"],
                        message,
                        clarification["reason"],
                        intent=intent,
                        tool=selected_tool,
                        confidence=confidence,
                        steps=planned_steps,
                        needs_clarification=clarification[
                            "needs_clarification"
                        ],
                        question=clarification["question"],
                        missing_arguments=clarification[
                            "missing_arguments"
                        ],
                    )

                return self._result(
                    False,
                    message,
                    argument_result.get(
                        "reason", "Argument extraction failed."
                    ),
                    intent=intent,
                    tool=selected_tool,
                    confidence=confidence,
                )

            if not argument_result.get("valid"):
                return self._result(
                    False,
                    message,
                    argument_result.get(
                        "reason", "Argument extraction failed."
                    ),
                    intent=intent,
                    tool=selected_tool,
                    confidence=confidence,
                )

            step["arguments"] = arguments

        return self._result(
            True,
            message,
            "Intelligence routing plan created. No tools were executed.",
            intent=intent,
            tool=selected_tool,
            confidence=confidence,
            steps=planned_steps,
        )

    def _result(
        self,
        valid,
        message,
        reason,
        intent=None,
        tool="none",
        confidence=None,
        steps=None,
        needs_clarification=False,
        question="",
        missing_arguments=None,
        ambiguity=None,
    ):
        return {
            "valid": valid,
            "message": message,
            "intent": intent,
            "tool": tool,
            "confidence": confidence,
            "steps": steps or [],
            "needs_clarification": needs_clarification,
            "question": question,
            "missing_arguments": missing_arguments or [],
            "ambiguity": ambiguity,
            "reason": reason,
            "executed": False,
        }
