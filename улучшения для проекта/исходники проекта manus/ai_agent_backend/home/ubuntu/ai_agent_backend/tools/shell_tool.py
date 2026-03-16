import subprocess

def run_shell_command_in_sandbox(command: str, sandbox_instance, timeout: int = 30) -> str:
    """Executes a shell command in a sandboxed environment and returns its output."""
    result = sandbox_instance.execute_command(command, timeout)
    if result["error"]:
        return f"Error: {result["error"]}\nStderr: {result["stderr"]}"
    return result["stdout"]

shell_tool_schema = {
    "name": "shell",
    "description": "Executes a shell command in a secure sandbox environment. Use it for file system operations, package installations, etc.",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to execute."
            }
        },
        "required": ["command"]
    }
}
