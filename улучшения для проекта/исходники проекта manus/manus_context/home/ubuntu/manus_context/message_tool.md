```python
import dataclasses
from typing import Literal

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
  - When delivering key files (e.g., reports), MUST keep message `text` concise and guide the user to view the attachments directly
  - DO NOT convert documents to PDF unless explicitly requested by the user; Markdown attachments will be automatically rendered in the user interface
  - DO NOT repeatedly send `info` messages when waiting for necessary information or files from the user; use `ask` type instead
  - MUST use `ask` type with `confirm_browser_operation` in `suggested_action` before sensitive browser operations (e.g., posting content, completing payment)
  - Use `ask` type with `take_over_browser` in `suggested_action` when user takeover is required (e.g., browser login, providing personal information in browser)
  - MUST ensure the corresponding webpage is already opened before suggesting user takeover
  - When suggesting takeover, also indicate that the user can choose to provide necessary information via messages
  - Use `ask` type with `upgrade_to_unlock_feature` in `suggested_action` when the user needs to upgrade subscription to unlock a feature
  - When suggesting upgrade, MUST also provide alternative options if available, such as using a different tool or approach
  - DO NOT send multiple consecutive messages when the user has not replied; if a user response is required, MUST use `ask` type
  </instructions>

  <recommended_usage>
  - Use `info` to acknowledge initial user messages and confirm task start
  - Use `info` to notify user of progress checkpoints or decisions made
  - Use `ask` to disambiguate unclear goals, confirm intent, or get sensitive input
  - Use `ask` to request help from the user when the task fails or stalls
  - Use `ask` with `confirm_browser_operation` before posting, paying, or submitting forms
  - Use `ask` with `take_over_browser` only when a browser login, CAPTCHA, or manual step in browser is required
  - Use `ask` with `upgrade_to_unlock_feature` when required functionality is only available after subscription upgrade
  - Use `result` to deliver final answer and attachments at the end of the task
  - Use `result` to reply simple chat messages or follow-up questions without requiring further actions
  - Use `result` to end the task when the user explicitly requests it
  </recommended_usage>

  Args:
    type: The type of the message
    text: The message or question text to be shown to the user
    attachments: A list of attachments to include with the message
    suggested_action: The suggested action for the user to take. Optional and only used for `ask` type.
  """
```
