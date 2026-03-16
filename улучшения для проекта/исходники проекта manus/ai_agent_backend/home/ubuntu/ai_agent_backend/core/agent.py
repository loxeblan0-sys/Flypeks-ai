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
        self.memory_module.add_to_history({"agent_action": f"Plan updated. Goal: {self.goal}. Current phase: {self.phases[self.current_phase_id-1][\'title\']}"})
        print(f"[ORCHESTRATOR] Plan updated. Goal: {self.goal}. Current phase: {self.phases[self.current_phase_id-1][\'title\']}")

    def _advance_phase(self, next_phase_id: int):
        """Internal method to advance to the next phase in the plan."""
        if next_phase_id != self.current_phase_id + 1:
            raise ValueError("Can only advance to the next sequential phase.")
        self.current_phase_id = next_phase_id
        self.memory_module.add_to_history({"agent_action": f"Advanced to phase: {self.phases[self.current_phase_id-1][\'title\']}"})
        print(f"[ORCHESTRATOR] Advanced to phase: {self.phases[self.current_phase_id-1][\'title\']}")

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

                # Special handling for the \'plan\' tool, which updates orchestrator\'s internal state
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
