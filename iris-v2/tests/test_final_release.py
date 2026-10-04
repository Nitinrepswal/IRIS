from core.platform import PlatformManager
from core.plugin_manager import PluginManager
from core.cloud_sync import CloudSync
from core.feedback import FeedbackSystem
from core.advanced_release import AdvancedRelease
from core.health import IRISHealth
from memory.memory_system import MemorySystem
from core.multimodal import MultiModalInput


def run_test(name, function):
    try:
        result = function()

        if result:
            print(f"PASS: {name}")
            return True

        print(f"FAIL: {name}")
        return False

    except Exception as error:
        print(f"FAIL: {name} -> {error}")
        return False


def test_platform():
    platform = PlatformManager()
    return platform.get_platform() != "Unknown"


def test_plugins():
    manager = PluginManager()
    manager.load()

    result = manager.execute(
        "hello",
        "Final release test"
    )

    return result["success"]


def test_cloud_sync():
    sync = CloudSync()

    sync.connect()

    result = sync.upload({
        "test": "IRIS"
    })

    sync.disconnect()

    return result["success"]


def test_feedback():
    feedback = FeedbackSystem(
        path="sandbox/final_feedback.json"
    )

    feedback.clear()

    feedback.add(
        "Final test",
        5,
        "Working"
    )

    result = feedback.get_average_rating()

    feedback.clear()

    return result == 5


def test_memory():
    memory = MemorySystem()

    memory.clear()

    memory.remember(
        "IRIS final release test memory"
    )

    memories = memory.get_all()

    memory.clear()

    return "IRIS final release test memory" in memories


def test_multimodal():
    multimodal = MultiModalInput()

    result = multimodal.execute(
        "text",
        "IRIS final test"
    )

    return (
        result.get("type") == "text"
        and result.get("content") == "IRIS final test"
    )


def test_advanced_release():
    release = AdvancedRelease()
    result = release.run()

    return result["release_ready"]


def test_health():
    health = IRISHealth()
    result = health.check_all()

    return result["status"] == "healthy"


def main():
    print("IRIS FINAL RELEASE TEST")
    print("=" * 50)

    tests = [
        ("Platform", test_platform),
        ("Plugins", test_plugins),
        ("Cloud Sync", test_cloud_sync),
        ("Feedback", test_feedback),
        ("Memory", test_memory),
        ("Multimodal", test_multimodal),
        ("Advanced Release", test_advanced_release),
        ("Runtime Health", test_health)
    ]

    passed = 0

    for name, function in tests:
        if run_test(name, function):
            passed += 1

    total = len(tests)

    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("IRIS FINAL TEST: PASS")
    else:
        print("IRIS FINAL TEST: FAIL")


if __name__ == "__main__":
    main()