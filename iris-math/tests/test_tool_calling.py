import json
import platform


def get_system_info():
    return {
        "system": platform.system(),
        "machine": platform.machine(),
        "python_version": platform.python_version()
    }


def get_greeting(name):
    return {
        "message": f"Hello, {name}!"
    }


tools = {
    "get_system_info": get_system_info,
    "get_greeting": get_greeting
}


tool_call = """
{
    "tool": "get_greeting",
    "arguments": {
        "name": "Nitin"
    }
}
"""


request = json.loads(tool_call)

tool_name = request["tool"]
arguments = request["arguments"]

print("Tool requested:")
print(tool_name)

print("\nArguments:")
print(arguments)

if tool_name not in tools:
    raise ValueError(f"Unknown tool: {tool_name}")

tool = tools[tool_name]

result = tool(**arguments)

print("\nTool result:")
print(result)