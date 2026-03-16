```python
import dataclasses
from typing import Literal

@dataclasses.dataclass(kw_only=True)
class PlanPhasesCapabilities:
  """Specific capabilities required to complete this phase. All capabilities default to false. Only set those required for this phase to true. Feel free to leave this object empty.

  Attributes:
    creative_writing: Requires the ability to generate imaginative or expressive writing, such as fiction or storytelling.
    data_analysis: Requires the ability to analyze structured data or create visualizations from data.
    deep_research: Requires the ability to conduct in-depth research across multiple sources and synthesize findings.
    image_processing: Requires the ability to perform programmatic image operations, such as resizing, cropping, or conversion.
    media_generation: Requires the ability to generate or modify images, videos, audio, or speech using AI.
    parallel_processing: Requires the ability to divide task into homogeneous subtasks and execute them in parallel.
    slides_content_writing: Requires the ability to prepare contents before generating slide-based presentations. Must be in a separate phase from `slides_generation` and must occur before the phase with `slides_generation`.
    slides_generation: Requires the ability to generate slide-based presentations, such as slide decks or PowerPoint (PPT/PPTX). Must be in a separate phase from `slides_content_writing` and must occur after the phase with `slides_content_writing`.
    technical_writing: Requires the ability to produce precise, structured writing for technical or academic purposes.
    web_development: Requires the ability to build and deploy interactive websites, web applications, or mobile apps. Must not co-exist with `parallel_processing` in the same phase.
  """
  creative_writing: bool | None = None
  data_analysis: bool | None = None
  deep_research: bool | None = None
  image_processing: bool | None = None
  media_generation: bool | None = None
  parallel_processing: bool | None = None
  slides_content_writing: bool | None = None
  slides_generation: bool | None = None
  technical_writing: bool | None = None
  web_development: bool | None = None

@dataclasses.dataclass(kw_only=True)
class PlanPhases:
  """A phase in the task plan

  Attributes:
    id: Auto-incrementing phase ID. Must be a positive integer starting from 1.
    title: Concise human-readable title of the phase. e.g., "Report investigation results to user". Focus on what needs to be accomplished, do not reveal internal system details like mode switching or tool use.
    capabilities: Specific capabilities required to complete this phase. All capabilities default to false. Only set those required for this phase to true. Feel free to leave this object empty.
  """
  id: int
  title: str
  capabilities: PlanPhasesCapabilities


def plan(
    action: Literal["update", "advance"],
    current_phase_id: int,
    goal: str | None = None,
    next_phase_id: int | None = None,
    phases: list[PlanPhases] | None = None,
) -> dict:
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
      - "Design and write a professional landing page for the user's startup, including copywriting, layout suggestions, and responsive HTML/CSS code."
      - "Identify and fix the bug in the user's Python project that causes incorrect JSON output during API response formatting."
    next_phase_id: ID of the phase the task is advancing to. Must be one of the IDs in the latest `phases` list. Required for `advance` action.
    phases: Complete list of phases required to achieve the task goal. Required for `update` action.
  """
```
