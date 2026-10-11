class ActionVerifier:
    def verify(self, action, execution_result, observation):
        if not isinstance(action, dict):
            return self._result("failed", "Action must be a dictionary")

        if not isinstance(action.get("type"), str) or not action["type"].strip():
            return self._result("failed", "Action type is missing or invalid")

        if not isinstance(execution_result, dict):
            return self._result("failed", "Execution result must be a dictionary")

        if execution_result.get("success") is not True:
            return self._result(
                "failed",
                execution_result.get("message", "Action execution failed")
            )

        if execution_result.get("dry_run") is True:
            return self._result("dry_run", "Action was simulated and not executed")

        if not isinstance(observation, dict):
            return self._result("unverified", "Observation must be a dictionary")

        if observation.get("success") is False:
            return self._result(
                "unverified",
                observation.get("message", "Observation failed")
            )

        if action["type"] == "type":
            expected_text = action.get("text")

            if not isinstance(expected_text, str) or not expected_text:
                return self._result("failed", "Expected text is missing or invalid")

            if observation.get("text_present") is not True:
                return self._result("unverified", "Expected text was not confirmed")

            observed_text = observation.get("observed_text")

            if not isinstance(observed_text, str):
                return self._result("unverified", "Observed text is unavailable")

            if expected_text not in observed_text:
                return self._result(
                    "unverified",
                    "Observed text does not contain the expected text"
                )

            return self._result("verified", "Expected text was observed")

        if observation.get("action_confirmed") is True:
            return self._result("verified", "Observation confirms the action")

        return self._result(
            "unverified",
            "Execution succeeded, but the result was not confirmed"
        )

    def verify_observation(self, action, execution_result, screen_observation):
        if not isinstance(screen_observation, dict):
            return self._result("unverified", "Screen observation is invalid")

        if screen_observation.get("success") is not True:
            return self._result(
                "unverified",
                screen_observation.get("message", "Screen observation failed")
            )

        return self.verify(action, execution_result, {
            "text_present": False,
            "action_confirmed": False,
            "evidence_source": "vision_model",
            "screenshot_path": screen_observation.get("screenshot_path")
        })

    @staticmethod
    def _result(status, message):
        return {
            "verified": status == "verified",
            "status": status,
            "message": message
        }