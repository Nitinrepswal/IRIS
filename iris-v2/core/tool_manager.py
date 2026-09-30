from core.app_control import AppControl
from core.file_control import FileControl
from core.web_control import WebControl
from core.system_control import SystemControl


class ToolManager:
    def __init__(self):
        self.app_control = AppControl()
        self.file_control = FileControl()
        self.web_control = WebControl()
        self.system_control = SystemControl()

    def execute(self, message):
        app_response = self.app_control.execute(message)
        if app_response is not None:
            return app_response

        file_response = self.file_control.execute(message)
        if file_response is not None:
            return file_response

        web_response = self.web_control.execute(message)
        if web_response is not None:
            return web_response

        system_response = self.system_control.execute(message)
        if system_response is not None:
            return system_response

        return None