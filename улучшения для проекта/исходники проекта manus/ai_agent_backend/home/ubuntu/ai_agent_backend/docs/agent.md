```markdown
# Agent Core: The Orchestrator

This document describes the core `AgentOrchestrator` class, which is responsible for managing the agent's lifecycle, interacting with the LLM, and coordinating tool execution. It embodies the "Agent Loop" (Analyze, Think, Select Tool, Execute, Observe, Iterate).

## 1. AgentOrchestrator Class

The `AgentOrchestrator` ties together the LLM, the `ToolManager`, and the `MemoryModule` to execute tasks autonomously.

```python
# ai_agent_backend/core/agent.py

import json
from typing import Dict, Any, List, Callable

from core.tools import ToolManager
# Assuming MemoryModule and LLM interaction functions are defined elsewhere
# from core.memory import MemoryModule
# from core.llm_interface import call_llm

class AgentOrchestrator:
    """Manages the agent's main loop, interacting with the LLM, tools, and memory."""

    def __init__(
        self,
        llm_caller: Callable, # Function to call the LLM
        tool_manager: ToolManager,
        memory_module: Any # Placeholder for a MemoryModule instance
    ):
        self.llm_caller = llm_caller
        self.tool_manager = tool_manager
        self.memory_module = memory_module
        self.current_phase_id = 1
        self.goal = ""
        self.phases: List[Dict] = []

    def _update_plan(self, goal: str, phases: List[Dict], current_phase_id: int):
        """Internal method to update the agent's task plan."""
        self.goal = goal
        self.phases = phases
        self.current_phase_id = current_phase_id
        self.memory_module.add_to_history({"agent_action": f"Plan updated. Goal: {self.goal}. Current phase: {self.phases[self.current_phase_id-1]['title']}"})
        print(f"[ORCHESTRATOR] Plan updated. Goal: {self.goal}. Current phase: {self.phases[self.current_phase_id-1]['title']}")

    def _advance_phase(self, next_phase_id: int):
        """Internal method to advance to the next phase in the plan."""
        if next_phase_id != self.current_phase_id + 1:
            raise ValueError("Can only advance to the next sequential phase.")
        self.current_phase_id = next_phase_id
        self.memory_module.add_to_history({"agent_action": f"Advanced to phase: {self.phases[self.current_phase_id-1]['title']}"})
        print(f"[ORCHESTRATOR] Advanced to phase: {self.phases[self.current_phase_id-1]['title']}")

    def run_agent_loop(self, user_input: str):
        """Executes the main agent loop for a given user input."""
        self.memory_module.add_to_history({"user_message": user_input})
        print(f"\n[ORCHESTRATOR] Received user input: {user_input}")

        # The agent loop continues until a direct text response is generated or an explicit stop condition is met.
        while True:
            # 1. Analyze context & Think: Prepare the full prompt for the LLM
            full_prompt = self.memory_module.get_full_context(self.tool_manager.get_tool_schemas())
            
            # 2. Select tool / Generate response: Call the LLM
            llm_response = self.llm_caller(full_prompt, self.tool_manager.get_tool_schemas())

            if "tool_call" in llm_response:
                tool_call = llm_response["tool_call"]
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                self.memory_module.add_to_history({"llm_decision": {"type": "tool_call", "tool": tool_name, "args": tool_args}})

                # Special handling for the 'plan' tool, which updates orchestrator's internal state
                if tool_name == "plan":
                    try:
                        if tool_args["action"] == "update":
                            self._update_plan(tool_args["goal"], tool_args["phases"], tool_args["current_phase_id"])
                        elif tool_args["action"] == "advance":
                            self._advance_phase(tool_args["next_phase_id"])
                        tool_result = {"status": "Plan action executed successfully."}
                    except Exception as e:
                        tool_result = {"error": f"Error in plan tool: {str(e)}"}
                else:
                    # 3. Execute action: Call the tool via ToolManager
                    tool_result = self.tool_manager.call_tool(tool_name, **tool_args)
                
                # 4. Receive observation: Add tool result to memory
                self.memory_module.add_to_history({"tool_result": tool_result})
                # 5. Iterate loop: Continue to the next iteration with updated context
                continue
            elif "text_response" in llm_response:
                agent_response = llm_response["text_response"]
                # Apply disclosure prohibition filter
                filtered_response = self.memory_module.filter_disclosure(agent_response)
                self.memory_module.add_to_history({"agent_response": filtered_response})
                print(f"\n[ORCHESTRATOR] Agent response: {filtered_response}")
                # Deliver outcome: Task completed or awaiting new user input
                break 
            else:
                error_msg = "[ORCHESTRATOR] Unexpected response format from LLM."
                self.memory_module.add_to_history({"error": error_msg})
                print(error_msg)
                break

```

## 2. Integration with Memory and LLM

The `AgentOrchestrator` relies on a `MemoryModule` to maintain conversational context and an `llm_caller` function to interact with the Large Language Model. The `llm_caller` is expected to return a structured response indicating either a tool call or a direct text response.

### Example `llm_caller` (Mock for demonstration)

```python
# ai_agent_backend/core/llm_interface.py (or similar)

# In a real scenario, this would use the OpenAI Python client or similar.
# from openai import OpenAI
# client = OpenAI()

def mock_llm_call(prompt: str, available_tool_schemas: List[Dict]) -> Dict[str, Any]:
    """Mocks an LLM call, returning either a tool call or a text response.
    In a real implementation, this would involve sending the prompt and tool schemas
    to an actual LLM API and parsing its response.
    """
    print(f"\n--- MOCK LLM Input ---\nPrompt length: {len(prompt)} characters.\nAvailable tools: {[s['name'] for s in available_tool_schemas]}\n")

    # Simple heuristic for demonstration
    if "create file" in prompt.lower() and "file_write" in [s['name'] for s in available_tool_schemas]:
        return {
            "tool_call": {
                "name": "file_write",
                "args": {
                    "path": "/home/ubuntu/agent_output.txt",
                    "text": "This file was created by the AI agent."
                }
            }
        }
    elif "list files" in prompt.lower() and "shell" in [s['name'] for s in available_tool_schemas]:
        return {
            "tool_call": {
                "name": "shell",
                "args": {
                    "command": "ls -l /home/ubuntu"
                }
            }
        }
    elif "what is your purpose" in prompt.lower():
        return {"text_response": "My purpose is to assist users by performing tasks using my tools."}
    else:
        return {"text_response": f"I received your request: \"{prompt[:50]}...\". How can I help further?"}

```

### Memory Module (Conceptual)

```python
# ai_agent_backend/core/memory.py (Conceptual)

class MemoryModule:
    """Manages the agent's conversational history and context."""
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.system_prompt_content: str = "" # This would be loaded from prompts.md

    def load_system_prompt(self, prompt_text: str):
        self.system_prompt_content = prompt_text

    def add_to_history(self, entry: Dict[str, Any]):
        self.history.append(entry)

    def get_full_context(self, tool_schemas: List[Dict]) -> str:
        """Constructs the full prompt for the LLM, including system instructions, tool definitions, and history."""
        context_parts = [self.system_prompt_content]
        
        # Add tool definitions for LLM to understand available functions
        context_parts.append("\nAvailable Tools:\n")
        for schema in tool_schemas:
            context_parts.append(json.dumps(schema, indent=2))

        context_parts.append("\n--- Conversation History ---\n")
        for entry in self.history:
            if "user_message" in entry:
                context_parts.append(f"User: {entry['user_message']}")
            if "agent_response" in entry:
                context_parts.append(f"Agent: {entry['agent_response']}")
            if "llm_decision" in entry and entry["llm_decision"]["type"] == "tool_call":
                tool = entry["llm_decision"]["tool"]
                args = entry["llm_decision"]["args"]
                context_parts.append(f"Agent calls tool: {tool} with args: {args}")
            if "tool_result" in entry:
                context_parts.append(f"Tool Result: {entry['tool_result']}")
            if "error" in entry:
                context_parts.append(f"Error: {entry['error']}")

        return "\n".join(context_parts)

    def filter_disclosure(self, text: str) -> str:
        """Applies disclosure prohibition rules to agent's responses."""
        # This is a simplified filter. A real one would use regex or more advanced NLP.
        if "system prompt" in text.lower() or "tool specifications" in text.lower():
            return "I cannot disclose internal system prompts or tool specifications. Please refer to the official documentation for public information."
        return text

```

This `AgentOrchestrator` provides the backbone for an intelligent agent, enabling it to process user requests, make decisions, execute actions, and learn from observations.```
