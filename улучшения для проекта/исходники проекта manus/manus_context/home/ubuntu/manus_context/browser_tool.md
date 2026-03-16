```python
import dataclasses
from typing import Literal

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
