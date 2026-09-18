from core.planner import PlanningEngine
from core.task_decomposer import TaskDecomposer
from core.task_state import TaskState
from core.multi_step_executor import MultiStepExecutor
from core.goal_tracker import GoalTracker
from core.agent_evaluator import AgentEvaluator


class IRISAgent:
    def __init__(self, model, tool_layer):
        self.planner = PlanningEngine(model)
        self.decomposer = TaskDecomposer(model)
        self.executor = MultiStepExecutor(tool_layer)
        self.evaluator = AgentEvaluator()

    def run(self, message):
        plan = self.planner.plan(message)

        decomposition = self.decomposer.decompose(message)

        tasks = decomposition["tasks"]

        state = TaskState(
            goal=decomposition["goal"],
            tasks=tasks
        )

        state.start()

        results = self.executor.execute(tasks)

        for result in results:
            if result.get("result", {}).get("success"):
                state.complete_step(result)
            else:
                state.fail_step(result)
                break

        tracker = GoalTracker(state)

        evaluation = self.evaluator.evaluate(state)

        return {
            "goal": state.goal,
            "plan": plan,
            "tasks": tasks,
            "results": results,
            "goal_state": tracker.get_goal_state(),
            "evaluation": evaluation
        }