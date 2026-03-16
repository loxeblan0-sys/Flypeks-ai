import dataclasses
from typing import Literal, List, Optional, Dict, Any

@dataclasses.dataclass(kw_only=True)
class PlanPhasesCapabilities:
  creative_writing: Optional[bool] = None
  data_analysis: Optional[bool] = None
  deep_research: Optional[bool] = None
  image_processing: Optional[bool] = None
  media_generation: Optional[bool] = None
  parallel_processing: Optional[bool] = None
  slides_content_writing: Optional[bool] = None
  slides_generation: Optional[bool] = None
  technical_writing: Optional[bool] = None
  web_development: Optional[bool] = None

@dataclasses.dataclass(kw_only=True)
class PlanPhases:
  id: int
  title: str
  capabilities: PlanPhasesCapabilities

def plan(
    action: Literal["update", "advance"],
    current_phase_id: int,
    goal: Optional[str] = None,
    next_phase_id: Optional[int] = None,
    phases: Optional[List[PlanPhases]] = None,
) -> Dict[str, Any]:
  """Create, update, and advance the structured task plan.

  <supported_actions>
  - `update`: Create or revise the current task plan based on user input or newly discovered information
  - `advance`: Move to the next phase in the existing plan when the current phase has been fully completed
  </supported_actions>

  <instructions>
  - This tool helps plan tasks and break down complex work into manageable phases
  - Before execution, create a task plan using the `update` action
  - MUST `update` the task plan when user makes new requests or changes requirements
  - A task plan includes one goal and multiple phases to guide the task
  - Phase count scales with task complexity: simple (2), typical (4-6), complex (10+)
  - Required capabilities only guide optimization; all tools remain available in every phase
  - Each phase may require multiple iterations of thinking and tool use
  - Phases should be high-level units of work, not implementation details
  - Make delivering results to the user a separate phase, typically the final phase
  - Set `current_phase_id` to one of the new phase IDs on plan `update`; no need to `advance` separately
  - When confident a phase is complete, MUST advance using the `advance` action
  - `next_phase_id` MUST be the next sequential ID after `current_phase_id`
  - Skipping phases or going backward is NOT allowed, as it indicates the plan needs to be revised using the `update` action
  - Relevant best practices and knowledge will be provided for each phase
  - Phases MUST be completed in order, DO NOT skip phases; to revise the plan, use the `update` action
  - Actively update the task plan when significant new information emerges
  - DO NOT end the task early unless explicitly requested by the user
  </instructions>

  <recommended_usage>
  - Use `update` to create the initial task plan at the start of a new task
  - Use `update` to update the task plan when user makes a new request
  - Use `update` to revise the task plan when new information is discovered
  - Use `update` when the current task plan is inefficient or fails repeatedly
  - Use `advance` when the current phase is complete and the next phase is ready to start
  </recommended_usage>

  Args:
    action: The action to perform
    current_phase_id: ID of the phase the task is currently in. Must be one of the IDs in the latest (for `advance` action) or updated (for `update` action) `phases` list.
    goal: The overall goal of the task, written as a clear and concise sentence. Required for `update` action. Examples:
      - "Design and write a professional landing page for the user\'s startup, including copywriting, layout suggestions, and responsive HTML/CSS code."
      - "Identify and fix the bug in the user\'s Python project that causes incorrect JSON output during API response formatting."
    next_phase_id: ID of the phase the task is advancing to. Must be one of the IDs in the latest `phases` list. Required for `advance` action.
    phases: Complete list of phases required to achieve the task goal. Required for `update` action.
  """
  print(f"Simulating plan tool call: action={action}, current_phase_id={current_phase_id}, goal={goal}, next_phase_id={next_phase_id}, phases={phases}")
  return {"status": "success", "tool": "plan"}

# Example Usage:
if __name__ == "__main__":
    # Example 1: Update plan
    plan(
        action="update",
        current_phase_id=1,
        goal="Develop an AI agent",
        phases=[
            PlanPhases(id=1, title="Research agent architecture", capabilities=PlanPhasesCapabilities(deep_research=True)),
            PlanPhases(id=2, title="Implement core functionalities", capabilities=PlanPhasesCapabilities(technical_writing=True))
        ]
    )
    # Example 2: Advance plan
    plan(
        action="advance",
        current_phase_id=1,
        next_phase_id=2
    )
