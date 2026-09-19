from tools.application import ApplicationTool
from tools.system import SystemTool
from tools.browser import BrowserTool


class ComputerControl:
    def __init__(self):
        self.application = ApplicationTool()
        self.system = SystemTool()
        self.browser = BrowserTool()

    def launch_application(self, application):
        return self.application.execute(
            application
        )

    def system_information(self):
        return self.system.execute()

    def open_webpage(self, url):
        return self.browser.execute(url)