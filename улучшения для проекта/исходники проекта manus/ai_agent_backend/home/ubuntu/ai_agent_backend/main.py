import os
import json
from typing import Dict, Any, List

# Import core components
from core.agent import AgentOrchestrator
from core.tools import ToolManager
from core.sandbox import Sandbox
from core.prompts import get_system_prompt

# Import tool definitions
from tools.shell_tool import run_shell_command_in_sandbox, shell_tool_schema
from tools.file_tool import write_to_file_in_sandbox, file_tool_schema

# --- LLM Interface (Mock or Real) ---
# For a real implementation, you would use the OpenAI client.
# from openai import OpenAI
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_llm_api(prompt: str, tool_schemas: List[Dict]) -> Dict[str, Any]:
    """Calls the actual LLM API with tool-calling capabilities."""
    print("\n--- Calling LLM API ---")
    # In a real implementation, you would use the actual API client here.
    # For demonstration, we reuse the mock from the agent.md file.
    if "create file" in prompt.lower() and "file_write" in [s["name"] for s in tool_schemas]:
        return {
            "tool_call": {
                "name": "file_write",
                "args": {
                    "path": "agent_output.txt",
                    "text": "This file was created by the AI agent."
                }
            }
        }
    elif "list files" in prompt.lower() and "shell" in [s["name"] for s in tool_schemas]:
        return {
            "tool_call": {
                "name": "shell",
                "args": {
                    "command": "ls -l"
                }
            }
        }
    elif "what is your purpose" in prompt.lower():
        return {"text_response": "My purpose is to assist users by performing tasks using my tools."}
    else:
        return {"text_response": f"I received your request. How can I help further?"}

# --- Memory Module (Conceptual) ---
class MemoryModule:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.system_prompt_content: str = ""

    def load_system_prompt(self, prompt_text: str):
        self.system_prompt_content = prompt_text

    def add_to_history(self, entry: Dict[str, Any]):
        self.history.append(entry)

    def get_full_context(self, tool_schemas: List[Dict]) -> str:
        context_parts = [self.system_prompt_content]
        context_parts.append("\nAvailable Tools:\n")
        for schema in tool_schemas:
            context_parts.append(json.dumps(schema, indent=2))
        context_parts.append("\n--- Conversation History ---\n")
        for entry in self.history:
            context_parts.append(str(entry))
        return "\n".join(context_parts)

    def filter_disclosure(self, text: str) -> str:
        if "system prompt" in text.lower() or "tool specifications" in text.lower():
            return "I cannot disclose internal system prompts or tool specifications."
        return text

# --- Main Application Setup ---
def main():
    print("Initializing AI Agent Backend...")

    # 1. Initialize Sandbox
    sandbox = Sandbox()

    # 2. Initialize ToolManager and register tools
    tool_manager = ToolManager()
    tool_manager.register_tool(
        "shell", 
        lambda command: run_shell_command_in_sandbox(command, sandbox), 
        shell_tool_schema
    )
    tool_manager.register_tool(
        "file_write", 
        lambda path, text: write_to_file_in_sandbox(path, text, sandbox), 
        file_tool_schema
    )

    # 3. Initialize Memory and load system prompts
    memory = MemoryModule()
    memory.load_system_prompt(get_system_prompt())

    # 4. Initialize Agent Orchestrator
    agent = AgentOrchestrator(
        llm_caller=call_llm_api,
        tool_manager=tool_manager,
        memory_module=memory
    )

    print("\nAI Agent is ready. Type your requests or \'exit\' to quit.")

    # 5. Start interactive loop
    while True:
        try:
            user_input = input("User > ")
            if user_input.lower() == "exit":
                break
            agent.run_agent_loop(user_input)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
