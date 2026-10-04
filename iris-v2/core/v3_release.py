from core.release import IRISRelease
from core.advanced_release import AdvancedRelease
from core.health import IRISHealth


class V3Release:
    def __init__(self):
        self.release = IRISRelease()
        self.advanced = AdvancedRelease()
        self.health = IRISHealth()

    def validate(self):
        release_status = self.release.get_status()

        advanced_result = self.advanced.run()
        health_result = self.health.check_all()

        release_ready = (
            self.release.is_ready()
            and advanced_result["release_ready"]
            and health_result["status"] == "healthy"
        )

        return {
            "version": release_status["version"],
            "codename": release_status["codename"],
            "platform": release_status["platform"],
            "capabilities": release_status["capabilities"],
            "plugins": release_status["plugins"],
            "advanced_tests": advanced_result,
            "health": health_result,
            "release_ready": release_ready
        }

    def get_summary(self):
        result = self.validate()

        return {
            "version": result["version"],
            "codename": result["codename"],
            "platform": result["platform"],
            "advanced_tests": (
                result["advanced_tests"]["passed"],
                result["advanced_tests"]["total"]
            ),
            "health": result["health"]["status"],
            "release_ready": result["release_ready"]
        }