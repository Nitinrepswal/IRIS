
import math
import time

from core.permission_control import PermissionControl


class MouseKeyboardController:
    def __init__(
        self,
        screen_width=1440,
        screen_height=900,
        dry_run=True,
        permission_control=None,
        require_confirmation=True,
    ):
        if (
            isinstance(screen_width, bool)
            or isinstance(screen_height, bool)
            or not isinstance(screen_width, int)
            or not isinstance(screen_height, int)
            or screen_width <= 0
            or screen_height <= 0
        ):
            raise ValueError("Screen dimensions must be positive integers")

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dry_run = dry_run
        self.permission_control = permission_control or PermissionControl()
        self.require_confirmation = require_confirmation
        self._backend = None

    def _valid_coordinates(self, x, y):
        if (
            isinstance(x, bool)
            or isinstance(y, bool)
            or not isinstance(x, (int, float))
            or not isinstance(y, (int, float))
            or not math.isfinite(x)
            or not math.isfinite(y)
        ):
            return False

        return (
            0 <= x < self.screen_width
            and 0 <= y < self.screen_height
        )

    def _get_backend(self):
        if self._backend is None:
            try:
                import pyautogui
            except ImportError as error:
                raise RuntimeError(
                    "Real computer control requires pyautogui"
                ) from error

            self._backend = pyautogui

        return self._backend

    
    
    def _authorize(self, action):
        action_names = {
            "move": "move",
            "click": "click",
            "type": "type",
            "press": "press"
        }

        policy_action = action_names.get(action)

        if policy_action is None:
            return {
                "success": False,
                "message": "Unsupported action"
            }

        try:
            allowed = self.permission_control.check("application")
        except Exception as error:
            return {
                "success": False,
                "message": f"Permission check failed: {error}"
            }

        if allowed is not True:
            return {
                "success": False,
                "message": "Computer control permission denied"
            }

        if self.require_confirmation:
            try:
                confirmed = self.permission_control.confirmation.confirm(
                    policy_action
                )
            except Exception as error:
                return {
                    "success": False,
                    "message": f"Confirmation failed: {error}"
                }

            if confirmed is not True:
                return {
                    "success": False,
                    "message": "Computer action was not approved"
                }

        return None


    def _perform(self, action, *args):
        if action not in {"move", "click", "type", "press"}:
            return {
                "success": False,
                "message": "Unsupported action"
            }

        denied = self._authorize(action)
        if denied is not None:
            return denied

        if self.dry_run:
            return {
                "success": True,
                "dry_run": True,
                "action": action
            }

        try:
            backend = self._get_backend()

            if action == "move":
                backend.moveTo(*args)
            elif action == "click":
                backend.click(*args)
            elif action == "type":
                self._type_with_shift(backend, args[0])
            elif action == "press":
                backend.press(*args)

            return {
                "success": True,
                "dry_run": False,
                "action": action
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"{type(error).__name__}: {error}"
            }

    def _type_with_shift(self, backend, text):
        for character in text:
            if character.isalpha() and character.isupper():
                backend.keyDown("shift")
                try:
                    backend.write(character.lower())
                finally:
                    backend.keyUp("shift")
            else:
                backend.write(character)

            time.sleep(0.03)

    def move_mouse(self, x, y):
        if not self._valid_coordinates(x, y):
            return {
                "success": False,
                "message": "Invalid screen coordinates"
            }

        return self._perform("move", x, y)

    def click_mouse(self, x, y, button="left"):
        if not self._valid_coordinates(x, y):
            return {
                "success": False,
                "message": "Invalid screen coordinates"
            }

        if button not in ("left", "right", "middle"):
            return {
                "success": False,
                "message": "Invalid mouse button"
            }

        moved = self.move_mouse(x, y)
        if not moved["success"]:
            return moved

        return self._perform("click", x, y, button)

    def type_text(self, text):
        if not isinstance(text, str) or not text.strip():
            return {
                "success": False,
                "message": "Text must be a non-empty string"
            }

        if len(text) > 1000:
            return {
                "success": False,
                "message": "Text exceeds the 1000-character limit"
            }

        return self._perform("type", text)

    def press_key(self, key):
        allowed_keys = {
            "enter", "tab", "esc", "escape", "space",
            "backspace", "delete", "up", "down", "left", "right",
            "home", "end", "pageup", "pagedown",
            "shift", "ctrl", "alt", "command",
            "f1", "f2", "f3", "f4", "f5", "f6",
            "f7", "f8", "f9", "f10", "f11", "f12"
        }

        if not isinstance(key, str) or not key.strip():
            return {
                "success": False,
                "message": "Key must be a non-empty string"
            }

        normalized_key = key.strip().lower()

        if len(normalized_key) == 1 and normalized_key.isalnum():
            return self._perform("press", normalized_key)

        if normalized_key not in allowed_keys:
            return {
                "success": False,
                "message": "Unsupported key"
            }

        if normalized_key == "escape":
            normalized_key = "esc"

        return self._perform("press", normalized_key)
