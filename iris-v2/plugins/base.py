class Plugin:
    name = "plugin"
    description = ""

    def execute(self, message):
        raise NotImplementedError