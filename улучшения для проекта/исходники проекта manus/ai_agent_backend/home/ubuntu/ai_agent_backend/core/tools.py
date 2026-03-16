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
            print(f"Warning: Tool \'{name}\' is already registered. Overwriting.")
        self.tools[name] = func
        self.tool_schemas.append(schema)
        print(f"Tool \'{name}\' registered successfully.")

    def get_tool_schemas(self) -> List[Dict]:
        """Returns the list of all tool schemas for the LLM prompt."""
        return self.tool_schemas

    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Calls a registered tool by name with the given arguments.

        In a real-world scenario, this would delegate the call to a secure sandbox
        environment to prevent malicious code execution.
        """
        if tool_name not in self.tools:
            return {"error": f"Tool \'{tool_name}\' not found."}

        try:
            print(f"Executing tool: {tool_name} with args: {kwargs}")
            # The actual function is called here.
            result = self.tools[tool_name](**kwargs)
            return {"result": result}
        except Exception as e:
            # Catching exceptions to prevent crashes and inform the agent.
            return {"error": f"Error executing tool {tool_name}: {str(e)}"}
