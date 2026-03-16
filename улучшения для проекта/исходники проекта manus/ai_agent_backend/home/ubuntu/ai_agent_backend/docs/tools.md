```markdown
# Tool System: Registration and Safe Execution

This document describes the architecture for a robust tool system that allows the AI agent to interact with its environment safely. It includes a `ToolManager` for registering and calling tools, and individual tool definitions.

## 1. ToolManager

The `ToolManager` is a central class responsible for holding all available tools, their schemas (for the LLM), and a safe mechanism to call them.

```python
# ai_agent_backend/core/tools.py

import json
from typing import Dict, Any, List, Callable

class ToolManager:
    """Manages the registration and execution of tools available to the agent."""

    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: List[Dict] = []

    def register_tool(self, name: str, func: Callable, schema: Dict):
        """Registers a tool, its function, and its JSON schema for the LLM."""
        if name in self.tools:
            print(f"Warning: Tool '{name}' is already registered. Overwriting.")
        self.tools[name] = func
        self.tool_schemas.append(schema)
        print(f"Tool '{name}' registered successfully.")

    def get_tool_schemas(self) -> List[Dict]:
        """Returns the list of all tool schemas for the LLM prompt."""
        return self.tool_schemas

    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Calls a registered tool by name with the given arguments.

        In a real-world scenario, this would delegate the call to a secure sandbox
        environment to prevent malicious code execution.
        """
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found."}

        try:
            print(f"Executing tool: {tool_name} with args: {kwargs}")
            # The actual function is called here.
            result = self.tools[tool_name](**kwargs)
            return {"result": result}
        except Exception as e:
            # Catching exceptions to prevent crashes and inform the agent.
            return {"error": f"Error executing tool ം{tool_name}ം: {str(e)}"}

```

## 2. Example Tool Definitions

Here are examples of how individual tools would be defined and then registered with the `ToolManager`. Each tool is a simple Python function, and its schema is a JSON object describing its purpose, parameters, and required arguments.

### Shell Tool

```python
# ai_agent_backend/tools/shell_tool.py

import subprocess

def run_shell_command(command: str, timeout: int = 30) -> str:
    """Executes a shell command in a sandboxed environment and returns its output."""
    try:
        # Using subprocess for execution. In a real system, this would be
        # heavily sandboxed (e.g., inside a Docker container with no network access).
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            check=True # Raise an exception for non-zero exit codes
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Command timed out."
    except subprocess.CalledProcessError as e:
        return f"Error: Command failed with exit code {e.returncode}\n{e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# JSON Schema for the shell tool
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
```

### File Write Tool

```python
# ai_agent_backend/tools/file_tool.py

def write_to_file(path: str, text: str) -> str:
    """Writes content to a specified file in the sandbox."""
    try:
        # In a real system, you would validate the path to ensure it stays within
        # the designated workspace directory.
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return f"File '{path}' written successfully."
    except Exception as e:
        return f"Error writing to file: {str(e)}"

# JSON Schema for the file write tool
file_tool_schema = {
    "name": "file_write",
    "description": "Writes or overwrites a text file at a specified path.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The absolute path of the file to write."
            },
            "text": {
                "type": "string",
                "description": "The content to write into the file."
            }
        },
        "required": ["path", "text"]
    }
}
```

## 3. Registration Process

In the main application setup, you would instantiate the `ToolManager` and register all your defined tools.

```python
# In main.py or a setup file

from core.tools import ToolManager
from tools.shell_tool import run_shell_command, shell_tool_schema
from tools.file_tool import write_to_file, file_tool_schema

def initialize_tool_manager() -> ToolManager:
    tool_manager = ToolManager()
    
    # Register all available tools
    tool_manager.register_tool("shell", run_shell_command, shell_tool_schema)
    tool_manager.register_tool("file_write", write_to_file, file_tool_schema)
    
    # ... register other tools here ...
    
    return tool_manager

# tool_manager = initialize_tool_manager()
```

This modular approach makes it easy to add, remove, or modify tools without changing the core logic of the agent orchestrator.
```
