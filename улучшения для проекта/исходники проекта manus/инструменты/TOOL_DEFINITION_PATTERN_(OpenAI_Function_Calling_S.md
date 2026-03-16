# TOOL DEFINITION PATTERN (OpenAI Function Calling Standard)

This is the standard format for defining tools that an LLM can call.
The LLM reads these definitions and decides autonomously when and how to use each tool.

---

## Basic Template

```python
from typing import Literal

def tool_name(
  required_param: str,
  optional_param: str = None,
) -> dict:
  """One-line description of what this tool does.

  When to use:
  - Describe the exact situation when this tool should be called
  - Be specific — vague descriptions lead to wrong tool selection

  Best practices:
  - List dos and don'ts for using this tool correctly
  - Mention edge cases the LLM should be aware of

  Args:
    required_param: Description of this parameter and what values it accepts
    optional_param: Description of this optional parameter and its default behavior

  Returns:
    Description of what the tool returns

  Tool category: [agent | search | file | browser | etc.]
  """
  ...
```

---

## Real Examples

### Shell Tool

```python
def shell_exec(
  session: str,
  command: str,
  timeout: int = 30,
) -> dict:
  """Execute a shell command in a sandboxed Linux environment.

  When to use:
  - When you need to run system commands, install packages, or execute scripts
  - When you need to interact with the file system via CLI

  Best practices:
  - Always use -y or -f flags to avoid interactive prompts
  - Chain commands with && to handle errors cleanly
  - Redirect large outputs to files instead of printing them

  Args:
    session: Unique identifier for the shell session
    command: The shell command to execute
    timeout: Timeout in seconds (default: 30)

  Tool category: agent
  """
  ...
```

### File Read Tool

```python
def file_read(
  path: str,
  range: list[int] = None,
) -> str:
  """Read the content of a file from the sandbox filesystem.

  When to use:
  - When you need to inspect the contents of a file
  - When you need to extract data from a text, code, or config file

  Best practices:
  - Do not read files you just wrote — their content is already in context
  - Use range parameter for large files to avoid token overflow

  Args:
    path: Absolute path to the file
    range: Optional [start_line, end_line] range to read

  Tool category: agent
  """
  ...
```

### Web Search Tool

```python
def web_search(
  queries: list[str],
  time: str = None,
) -> list[dict]:
  """Search the web and return results.

  When to use:
  - When you need up-to-date information not available in training data
  - When the user asks about current events, prices, or real-time data

  Best practices:
  - Provide up to 3 query variants that express the same intent
  - Use time filter only when recency is explicitly required

  Args:
    queries: Up to 3 query variants expressing the same search intent
    time: Optional filter — one of: "past_day", "past_week", "past_month", "past_year"

  Returns:
    List of results, each with title, url, and snippet

  Tool category: search
  """
  ...
```

---

## How to Pass Tools to the LLM (OpenAI API)

```python
import openai
import json

client = openai.OpenAI()

tools = [
  {
    "type": "function",
    "function": {
      "name": "web_search",
      "description": "Search the web and return results.",
      "parameters": {
        "type": "object",
        "properties": {
          "queries": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Up to 3 query variants"
          },
          "time": {
            "type": "string",
            "enum": ["past_day", "past_week", "past_month", "past_year"],
            "description": "Optional time filter"
          }
        },
        "required": ["queries"]
      }
    }
  }
]

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "What is the latest news about AI?"}],
  tools=tools,
  tool_choice="auto"
)
```
