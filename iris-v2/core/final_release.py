from core.v3_release import V3Release


class FinalRelease:
    def __init__(self):
        self.release = V3Release()

    def run(self):
        try:
            result = self.release.validate()

            return {
                "success": True,
                "version": result["version"],
                "codename": result["codename"],
                "platform": result["platform"],
                "release_ready": result["release_ready"]
            }

        except Exception as error:
            return {
                "success": False,
                "version": "3.0.0",
                "codename": "IRIS V3.0",
                "platform": "Unknown",
                "release_ready": False,
                "error": str(error)
            }

    def is_ready(self):
        result = self.run()

        return (
            result["success"]
            and result["release_ready"]
        )