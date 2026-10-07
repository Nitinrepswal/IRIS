import importlib


MODULES = [
    "app.main",
    "app.window",
    "app.chat",
    "app.worker",
    "app.voice",
    "app.voice_output",

    "core.iris_core",
    "core.iris_brain",
    "core.nlu",
    "core.conversation",
    "core.intent",
    "core.tool_selector",

    "core.planner",
    "core.task_decomposer",
    "core.multi_step_executor",
    "core.autonomous_task",
    "core.observer",
    "core.recovery",
    "core.task_state",

    "core.tool_registry",
    "core.tool_layer",
    "core.tool_manager",

    "core.app_control",
    "core.file_control",
    "core.web_control",
    "core.system_control",
    "core.computer_control",

    "core.permission",
    "core.permission_control",
    "core.confirmation",
    "core.sandbox",

    "core.screenshot",
    "core.vision",
    "core.multimodal",
    "core.web_knowledge",

    "core.platform",
    "core.plugin_manager",
    "core.cloud_sync",
    "core.feedback",

    "core.advanced_release",
    "core.health",

    "models.llm_model",

    "memory.memory_system",
    "memory.long_term_memory",
    "memory.working_memory",
    "memory.profile",
    "memory.conversation_store",
    "memory.knowledge_base",

    "tools.web_search",
    "tools.web_retriever",
    "tools.filesystem",
    "tools.file_reader",
    "tools.file_editor",

    "plugins.base",
    "plugins.hello_plugin"
]


def main():
    print("IRIS V3.1 ARCHITECTURE AUDIT")
    print("=" * 60)

    passed = 0
    failed = []

    for module_name in MODULES:
        try:
            importlib.import_module(module_name)

            print(f"PASS: {module_name}")
            passed += 1

        except Exception as error:
            print(f"FAIL: {module_name}")
            print(f"      {error}")

            failed.append(module_name)

    total = len(MODULES)

    print("\n" + "=" * 60)
    print(f"Modules checked: {total}")
    print(f"Modules passed:  {passed}")
    print(f"Modules failed:  {len(failed)}")

    if failed:
        print("\nFailed modules:")

        for module in failed:
            print(f"- {module}")

    print("\n" + "=" * 60)

    if not failed:
        print("ARCHITECTURE AUDIT: PASS")
    else:
        print("ARCHITECTURE AUDIT: FAIL")


if __name__ == "__main__":
    main()