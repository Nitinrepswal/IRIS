class CloudSync:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
        return {
            "success": True,
            "message": "Cloud sync connected."
        }

    def disconnect(self):
        self.connected = False
        return {
            "success": True,
            "message": "Cloud sync disconnected."
        }

    def is_connected(self):
        return self.connected

    def upload(self, data):
        if not self.connected:
            return {
                "success": False,
                "message": "Cloud sync is not connected."
            }

        return {
            "success": True,
            "message": "Data ready for cloud upload.",
            "data": data
        }

    def download(self):
        if not self.connected:
            return {
                "success": False,
                "message": "Cloud sync is not connected."
            }

        return {
            "success": True,
            "message": "No cloud data available."
        }