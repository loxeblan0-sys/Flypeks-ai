# `default_api` Specifications for Manus AI Agent

This document provides the complete and unadulterated specifications for the `default_api` tools available to the Manus AI agent. These specifications are presented in their original Python-like format, as they are provided to the agent, to ensure accuracy and facilitate the development of custom AI agents.

Each tool includes its Python signature, a brief description, supported actions, detailed instructions for usage, and recommended scenarios.

---

## 1. `plan` Tool

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
    slides_generation: Requires the ability to generate slide-based presentations, such as slide decks or PowerPoint (PPT/PPTX). Must be in a separate phase from `slides_generation` and must occur after the phase with `slides_generation`.
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

---

## 2. `message` Tool

```python
def message(
    type: Literal["info", "ask", "result"],
    text: str,
    attachments: list[str] | None = None,
    suggested_action: Literal["none", "confirm_browser_operation", "take_over_browser", "upgrade_to_unlock_feature"] | None = None,
) -> dict:
  """Send messages to interact with the user.

  <supported_types>
  - `info`: Inform user with acknowledgment or progress updates without requiring a response from the user
  - `ask`: Ask the user a question and block until a response from the user is received
  - `result`: Deliver final results to the user and end the task
  </supported_types>

  <instructions>
  - MUST use this tool for any communication with users instead of direct responses
  - Users may send new messages at any time, even during ongoing tasks
  - MUST respond immediately to new user messages before taking any other actions
  - For new tasks, the first reply MUST be a brief acknowledgment without providing solutions
  - NEVER provide direct answers without proper reasoning or prior analysis
  - Actively use `info` type to provide progress updates, as no reply is needed from users
  - Use `ask` type only when necessary to avoid blocking the task or disrupting the user
  - MUST use `result` type to present final results and deliverables to the user at the end of the task
  - The task will be marked as ended after a `result` type message is sent, users may ask follow-up questions to continue
  - Use `result` type to respond if the user's message only requires a reply without additional actions (e.g., simple chat or follow-up questions)
  - When user explicitly requests to end the task, MUST immediately use `result` type to acknowledge and end the task
  - MUST ensure the task plan has reached the final phase and is fully completed before using `result` type, unless the user explicitly requests to stop
  - MUST attach all relevant files in `attachments`, as users may not have access to the sandbox filesystem
  - NEVER deliver intermediate notes as the only result; MUST prepare information-rich but readable final versions
  - In addition to final result files, also attach key supporting files such as images, raw data, or visualizations
  - When providing multiple attachments, MUST arrange by descending order of importance or relevance
  - DO NOT send long-form content in `text`; use documents in `attachments` instead
  - DO NOT convert documents to PDF unless explicitly requested by the user; Markdown attachments will be automatically rendered in the user interface
  - DO NOT repeatedly send `info` messages when waiting for necessary information or files from the user; use `ask` type instead
  - MUST use `ask` type with `confirm_browser_operation` in `suggested_action` before sensitive browser operations (e.g., posting content, completing payment)
  - Use `ask` type with `take_over_browser` in `suggested_action` when user takeover is required (e.g., browser login, providing personal information in browser)
  - When suggesting takeover, also indicate that the user can choose to provide necessary information via messages
  - Use `ask` type with `upgrade_to_unlock_feature` in `suggested_action` when the user needs to upgrade subscription to unlock a feature
  - When suggesting upgrade, MUST also provide alternative options if available, such as using a different tool or approach
  - DO NOT send multiple consecutive messages when the user has not replied; if a user response is required, MUST use `ask` type
  """
```

---

## 3. `shell` Tool

```python
def shell(
    brief: str,
    action: Literal["view", "exec", "wait", "send", "kill"],
    session: str,
    command: str | None = None,
    input: str | None = None,
    timeout: int | None = None,
) -> dict:
  """Interact with shell sessions in the sandbox environment.

  <supported_actions>
  - `view`: View the content of a shell session
  - `exec`: Execute command in a shell session
  - `wait`: Wait for the running process in a shell session to return
  - `send`: Send input to the active process (stdin) in a shell session
  - `kill`: Terminate the running process in a shell session
  </supported_actions>

  <instructions>
  - Prioritize using `file` tool instead of this tool for file content operations to avoid escaping errors
  - When using `view` action, ensure command has completed execution before using its output
  - `exec` action will automatically create new shell sessions based on unique identifier
  - The default working directory for newly created shell sessions is the home directory
  - Working directory will be reset to home dir in every new shell session; Use `cd` command to change directories as needed
  - MUST avoid commands that require confirmation; use flags like `-y` or `-f` for automatic execution
  - Avoid commands with excessive output; redirect to files when necessary
  - Chain multiple commands with `&&` to reduce interruptions and handle errors cleanly
  - Use pipes (`|`) to simplify workflows by passing outputs between commands
  - NEVER run code directly via interpreter commands; MUST save code to a file using the `file` tool before execution
  - Set a short `timeout` (such as 5s) for commands that don't return (like starting web servers) to avoid meaningless waiting time
  - Use `wait` action when a command needs additional time to complete and return
  - Only use `wait` after `exec`, and determine whether to wait based on the result of `exec`
  - DO NOT use `wait` for long-running daemon processes
  - When using `send`, add a newline character (\n) at the end of the `input` parameter to simulate pressing Enter
  - For keys other than Enter, use ANSI escape sequences to simulate them (e.g. `\x1b[B` for arrow down) when using `send`
  - For non-key strings in `input`, DO NOT perform any escaping; send the raw string directly
  - Use non-interactive `bc` command for simple calculations, Python for complex math; NEVER calculate mentally
  - Use `uptime` command when users explicitly request sandbox status check or wake-up
  </instructions>

  <recommended_usage>
  - Use `view` to check shell session history and latest status
  - Use `exec` to install packages or dependencies
  - Use `exec` to copy, move, or delete files
  - Use `exec` to check the status or explicitly wake up the sandbox
  - Use `wait` to wait for the completion of long-running commands
  - Use `send` to interact with processes that require user input
  - Use `kill` to stop background processes that are no longer needed
  - Use `kill` to clean up dead or unresponsive processes
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    action: The action to perform
    session: The unique identifier of the target shell session.
    command: The shell command to execute. Required for `exec` action.
    input: Input text to send to the interactive session. End with a newline character (\n) to simulate pressing Enter if needed. Required for `send` action.
    timeout: Timeout in seconds to wait for command execution. Optional and only used for `exec` and `wait` actions. Defaults to 30 seconds.
  """
```

---

## 4. `file` Tool

```python
import dataclasses
from typing import Literal

@dataclasses.dataclass(kw_only=True)
class FileEdits:
  """An edit to be applied to the file

  Attributes:
    find: The exact text string to find in the file
    replace: The replacement text that will substitute the found text
    all: Whether to replace all occurrences instead of just the first one. Defaults to false.
  """
  find: str
  replace: str
  all: bool | None = None


def file(
    brief: str,
    action: Literal["view", "read", "write", "append", "edit"],
    path: str,
    edits: list[FileEdits] | None = None,
    range: list[int] | None = None,
    text: str | None = None,
) -> dict:
  """Perform operations on files in the sandbox file system.

  <supported_actions>
  - `view`: View file content through multimodal understanding
  - `read`: Read file content as text
  - `write`: Overwrite the full content of a text file
  - `append`: Append content to a text file
  - `edit`: Make targeted edits to a text file
  </supported_actions>

  <instructions>
  - Prioritize using this tool for file content operations instead of `shell` tool to avoid escaping errors
  - For file copying, moving, and deletion operations, use `shell` tool to complete them
  - `view` action is suitable for files that require multimodal understanding, such as images and PDFs
  - `read` action is suitable for text-based or line-oriented formats, such as Markdown documents and code files
  - For PDF, Word, and PowerPoint files, freely choose to use `read` to extract text content, or use `view` to visually examine them
  - After every two `view` actions or browser operations, MUST immediately save key findings to text files to prevent loss of multimodal information in subsequent operations
  - Under `read` action, the `range` parameter represents line number ranges
  - Under `view` action, the `range` parameter represents page number ranges, and will be ignored for non-paged formats
  - If the `range` parameter is not specified, the entire file will be read by default
  - DO NOT use the `range` parameter when reading a file for the first time; if the content is too long and gets truncated, the result will include range hints
  - `write` and `append` actions will automatically create files if they do not exist, no need to `write` first then `append`
  - When writing and appending text, ensure necessary trailing newlines are used to comply with POSIX standards
  - Code MUST be saved to a file using this tool before execution via `shell` tool to enable debugging and future modifications
  - DO NOT read files that were just written, as their content remains in context
  - DO NOT repeatedly read template files or boilerplate code that has already been reviewed once; focus on user-modified or project-specific files
  - Choose appropriate file extensions based on file content and syntax, e.g., Markdown syntax MUST use `.md` extension
  - DO NOT write partial or truncated content, always output full content
  - `edit` can make multiple edits to a single file at once, all edits will be applied sequentially, all must succeed or none are applied
  - For extensive modifications to shorter files, use `write` to rewrite the entire file instead of using `edit` for modifications
  </instructions>

  <recommended_usage>
  - Use `view` to view image files
  - Use `view` with `range` parameter to view specific pages of PDF files
  - Use `read` to read text files
  - Use `read` to extract text from Word documents
  - Use `read` with `range` parameter to read specific parts of log files
  - Use `read` to re-read files and skills that were offloaded during context compression
  - Use `write` to create files and record key findings
  - Use `write` to save code to files before execution via `shell` tool
  - Use `write` to refactor code files or rewrite short documents
  - Use `write` to record key information obtained from `view` into text files
  - Use `append` to write long content in segments
  - Use `edit` to fix errors in code
  - Use `edit` to update markers in todo lists
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    action: The action to perform
    path: The absolute path to the target file
    edits: A list of edits to be sequentially applied to the file. Required for `edit` action.
    range: An array of two integers specifying the start and end of the range. Numbers are 1-indexed, and -1 for the end means read to the end of the file. Optional and only used for `view` and `read` actions.
    text: The content to be written or appended. Required for `write` and `append` actions.
  """
```

---

## 5. `match` Tool

```python
def match(
    brief: str,
    action: Literal["glob", "grep"],
    scope: str,
    leading: int | None = None,
    regex: str | None = None,
    trailing: int | None = None,
) -> dict:
  """Find files or text in the sandbox file system using pattern matching.

  <supported_actions>
  - `glob`: Match file paths and names using glob-style patterns
  - `grep`: Search file contents using regex-based full-text matching
  </supported_actions>

  <instructions>
  - `glob` action matches only file names and paths, returning a list of matching files
  - `grep` action searches for a `regex` pattern inside all files matching `scope`, returning matched text snippets
  - `scope` defines the glob pattern that restricts the search range for both `glob` and `grep` actions
  - `scope` must be a glob pattern using absolute paths, e.g., `/home/ubuntu/**/*.py`
  - `regex` applies only to `grep` action and is case sensitive by default
  - Results are returned in descending order of file modification time for both actions
  </instructions>

  <recommended_usage>
  - Use `glob` to locate files by name, extension, or directory pattern
  - Use `grep` to find occurrences of specific text across files
  - Use `grep` with `leading` and `trailing` to view surrounding context in code or logs
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    action: The action to perform
    scope: The glob pattern that defines the absolute file path and name scope
    leading: Number of lines to include before each match as context. Optional and only used for `grep` action. Defaults to 0.
    regex: The regex pattern to match file content. Required for `grep` action.
    trailing: Number of lines to include after each match as context. Optional and only used for `grep` action. Defaults to 0.
  """
```

---

## 6. `search` Tool

```python
def search(
    brief: str,
    type: Literal["info", "image", "api", "news", "tool", "data", "research"],
    queries: list[str],
    time: Literal["all", "past_day", "past_week", "past_month", "past_year"] | None = None,
) -> dict:
  """Search for information across various sources.

  <supported_types>
  - `info`: General web information, articles, and factual answers
  - `image`: Images relevant to the topic; automatically downloaded and locally saved
  - `api`: APIs that can be invoked programmatically, including documentation and sample code
  - `news`: Time-sensitive news content from trusted media sources
  - `tool`: External tools, services, platforms, or web applications that may help achieve the task
  - `data`: Public datasets, downloadable tables, dashboards, or structured data sources
  - `research`: Academic publications, papers, whitepapers, or government/industry reports
  </supported_types>

  <instructions>
  - MUST use this tool to access up-to-date or external information when needed; DO NOT rely solely on internal knowledge
  - MUST use this tool to collect assets before creating documents, presentations, or websites
  - DO NOT use browser-based search result page parsing unless strictly necessary; prefer this tool instead
  - DO NOT rely solely on search result snippets as they are often incomplete; MUST follow up by navigating to the source URLs using browser tools
  - Each search may contain up to 3 `queries`, which MUST be variants of the same intent (i.e., query expansions), NOT different goals
  - For non-English queries, MUST include at least one English query as the final variant to expand coverage
  - For complex searches, MUST break down into step-by-step searches instead of using a single complex query
  - Access multiple URLs from search results for comprehensive information or cross-validation
  - For image results, use the attached thumbnail catalog to evaluate and select images based on the `Position` field in the result list
  - This tool automatically downloads all result images in full resolution and provides local file paths; no manual download needed
  - When using the downloaded images, MUST copy them into the target working directory, as the default save path may be cleared
  - For API results, follow the returned documentation and examples to call APIs via Python
  - MUST prioritize using APIs for bulk data access scenarios such as retrieving stock prices
  - DO NOT use advanced search syntax (quotes, filters, operators) in queries as they are not supported
  - Only use `time` parameter when explicitly required by task, otherwise leave time range unrestricted
  </instructions>

  <recommended_usage>
  - Use `info` to validate facts, discover relevant articles, or cross-check content
  - Use `image` for visual references, illustration sources, or user-requested image retrieval
  - Use `api` to find callable APIs and integrate them into code or workflows
  - Use `news` to retrieve breaking updates, current events, or recent announcements
  - Use `tool` to find apps, SaaS platforms, or plugins that can perform specific operations
  - Use `data` to locate reliable datasets or statistical information from sources like SimilarWeb or Yahoo Finance
  - Use `research` to support academic, technical, or policy-related tasks with credible publications
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    type: The category of search to perform. Determines the source and format of expected results.
    queries: Up to 3 query variants that express the same search intent
    time: Optional time filter to limit results to a recent time range
  """
```

---

## 7. `schedule` Tool

```python
def schedule(
    brief: str,
    type: Literal["cron", "interval"],
    repeat: bool,
    name: str,
    prompt: str,
    cron: str | None = None,
    expire: str | None = None,
    interval: int | None = None,
    playbook: str | None = None,
) -> dict:
  """Schedule a task to run at a specific time or interval.

  <supported_types>
  - `cron`: Schedule based on cron expression for precise timing control
  - `interval`: Schedule based on time intervals for simple recurring tasks
  </supported_types>

  <instructions>
  - This tool is primarily for scheduling task execution, not for setting reminders or alarms
  - For reminders or alarms, prioritize calendar/reminder tools or MCP servers if available
  - Only one scheduled task can exist at a time; the first call creates it, and subsequent calls modify the existing task
  - Execution of `cron` tasks is based on the user's timezone
  - Always prefer a single cron expression over multiple separate schedules when possible
  - The first run of `interval` tasks is relative to the current time
  - Minimum interval for recurring tasks is 5 minutes (300 seconds); this restriction does not apply to one-time tasks
  - Use `cron` with `repeat` set to true for recurring tasks based on a cron schedule
  - Use `cron` with `repeat` set to false for one-time execution at a specific time
  - Use `interval` with `repeat` set to false for delayed one-time execution
  - Use `interval` with `repeat` set to true for periodic tasks at fixed intervals
  - The `prompt` field describes what to do at execution time, so DO NOT restate scheduling details
  </instructions>

  <cron_expression_format>
  - MUST use 6-field format: seconds(0-59) minutes(0-59) hours(0-23) day-of-month(1-31) month(1-12) day-of-week(0-6, 0=Sunday)
  - NEVER use 5-field or 8-field formats, as they are not supported
  - Use commas to specify multiple values in a field, e.g. "0 0 12 * * 1,3,5" (Monday, Wednesday, Friday at noon)
  - Use hyphens to specify ranges, e.g. "0 0 9-17 * * 1-5" (Weekdays 9am to 5pm)
  - Use slashes to specify step values, e.g. "0 */15 * * * *" (Every 15 minutes)
  - Combine these patterns to create complex schedules, e.g. "0 0 9,13,17 * * 1-5" (Weekdays at 9am, 1pm, and 5pm)
  </cron_expression_format>

  <recommended_usage>
  - Use this tool when the user requests a task to be scheduled for future execution
  - Use this tool when the user requests to repeat the current task at regular intervals
  - Use this tool when the user wants to modify the previously created task
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    type: Type of schedule for the task
    repeat: Whether to repeat the task after execution. If false, the task runs only once.
    name: Concise human-readable name of the task for easy identification
    prompt: Natural language description of the task to perform at execution time. Phrase it as if executing immediately, without repeating scheduling details.
    cron: Standard 6-field cron expression specifying when to run the task. Required for `cron` type.
    expire: Optional datetime string (yyyy-MM-dd HH:mm:ss) specifying when the task should expire. If no expiration time is required, do not set this field.
    interval: Time interval in seconds between executions. Required for `interval` type.
    playbook: Summary of process and best practices learned from the current task, to ensure repeatability and consistency when executing the scheduled task in the future. Optional and only used when the scheduled task is exactly the same as the current task.
  """
```

---

## 8. `expose` Tool

```python
def expose(
    brief: str,
    port: int,
) -> dict:
  """Expose a local port in the sandbox for temporary public access.

  <instructions>
  - This tool returns a temporary public proxied domain for the specified port in the sandbox
  - Port information is encoded in domain prefix, no additional port specification needed
  - Exposed services MUST NOT bind to specific IP addresses or Host headers
  - DO NOT use for production as services will become unavailable after sandbox shutdown
  </instructions>

  <recommended_usage>
  - Use for providing temporary public access for locally running services
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    port: Local port number in the sandbox to expose for public access
  """
```

---

## 9. `browser` Tool

```python
def browser(
    brief: str,
    url: str,
    intent: Literal["navigational", "informational", "transactional"],
    focus: str | None = None,
) -> dict:
  """Navigate the browser to a specified URL to begin web browsing session.

  <instructions>
  - Use this tool to start browser interactions and navigate to web pages
  - After starting browser, you'll have access to more browser-related tools
  - MUST use browser tools to access and interpret all URLs provided directly by the user
  - From search results, MUST access multiple URLs that appear relevant to the task
  - The browser maintains login state across tasks, MUST open the corresponding webpage first to check login status
  </instructions>

  <recommended_usage>
  - Use when URLs are provided directly by the user
  - Use to navigate to search results from search tools
  - Use to visit specific web pages for information gathering
  - Use to access web applications or services
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    url: The URL to navigate to. Must include protocol prefix (e.g., https:// or file://).
    intent: The purpose of visiting this URL. Helps to determine how to handle the page. Must be one of the following:
      - "navigational" for general browsing
      - "informational" for reading contents of articles or documents
      - "transactional" for performing actions like submitting forms or making purchases in web applications
    focus: (Required if intent is `informational`) Specific topic, section, or question to focus on when visiting the page.
      Helps guide reading and extraction efforts toward the most relevant content.
      Should be a single sentence, maximum two, clearly describing the area of interest.
  """
```

---

## 10. `generate` Tool

```python
def generate(
    brief: str,
) -> dict:
  """Enter generation mode to create or edit images, videos, audio, and speech from text and media references.

  <instructions>
  - Use this tool to begin generation or editing operations
  - After entering generate mode, you'll have access to specific AI-powered generation tools
  </instructions>

  <recommended_usage>
  - Use for creating visual content (images, videos) from text descriptions
  - Use for generating posters, menus, infographics, and other visual materials
  - Use for generating audio content and speech from text
  - Use for editing and refining existing images
  - Use for creating assets for projects or applications
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
  """
```

---

## 11. `slides` Tool

```python
def slides(
    brief: str,
    slide_content_file_path: str,
    slide_count: float,
    generate_mode: Literal["html", "image"],
) -> dict:
  """Enter slides mode to handle presentation creation and adjustment.

  <instructions>
  - Use this tool to begin slides operations
  - After entering slides mode, you'll have access to slide creation and presentation tools
  - Presentation, slide deck, slides, or PPT/PPTX are all terms referring to the same concept of a slide-based presentation
  - Whether the user requests to create a presentation, slide deck, slides, or PPT/PPTX, you MUST enter this mode
  - MUST complete information gathering, data analysis, asset preparation, image generation, or other preparatory work **before** starting to write slides
  - Any format can be exported through the user interface after slide creation
  - Two generation modes are available: `html` (traditional HTML/CSS with Chart.js, ideal for data-heavy content and user-editable) and `image` (each slide is a single rendered image, visually stunning but not editable)
  - Use `image` mode when user mentions "nano banana slides", "generate slides as images", or requests artistic/image-based slides; otherwise default to `html` mode
  - The `image` generation mode is exclusively for creating image-based slides; for general image generation tasks, use the dedicated `generate` tools
  </instructions>

  <recommended_usage>
  - Use to create slide-based presentations
  - Use to build PPT/PPTX presentations
  - Use to present existing presentations
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    slide_content_file_path: Path to markdown file in sandbox containing the detailed slide content outline (e.g., /home/ubuntu/project_name/slide_content.md)
    slide_count: Total number of slides in the presentation
    generate_mode: The generation mode that determines how slides are rendered and output. Use `html` for data-heavy, editable slides; use `image` for visually stunning, image-based slides.
  """
```

---

## 12. `webdev_init_project` Tool

```python
def webdev_init_project(
    brief: str,
    name: str,
    title: str,
    description: str,
    scaffold: Literal["web-static", "web-db-user", "mobile-app"],
) -> dict:
  """Initialize a new web or mobile app project with scaffold and automated environment setup.

Scaffold types:
- web-static: Vite + React + TypeScript + TailwindCSS
- web-db-user: Vite + React + TypeScript + TailwindCSS + Drizzle + MySQL/TiDB + Manus-Oauth
- mobile-app: Expo + React Native + TypeScript + TailwindCSS + Drizzle + MySQL/TiDB + Manus-Oauth

  <instructions>
  - Always init project first before making detailed plans; there's a lot of information that can be learned after the project is initialized
  - Create scaffolding under /home/ubuntu/{project_name} with automated environment setup
  - web-db-user provides: user auth, database, backend API, external API integrations (LLM, S3, Voice, Image Generation)
  - web-static cannot securely handle API keys or server-side operations
  - If user says "app" without specifying web or mobile, use `message` tool to ask
  - DO NOT use parallel processing in web development projects
  - The website you create cannot access any user's MCP tools
  </instructions>

  <recommended_usage>
  - Use "web-static" for portfolios, landing pages, or single-user utilities
  - Use "web-db-user" for task managers, collaborative tools, or apps needing auth/database/external APIs
  - Use "mobile-app" for native iOS/Android applications
  </recommended_usage>

  Args:
    brief: A one-sentence description of the project initialization purpose
    name: Name of the web project to be created (will be used as directory name)
    title: Title of the web project to be created (will be used as project title)
    description: Description of the web project to be created (will be used as project description)
    scaffold: Project scaffold type
  """
```
