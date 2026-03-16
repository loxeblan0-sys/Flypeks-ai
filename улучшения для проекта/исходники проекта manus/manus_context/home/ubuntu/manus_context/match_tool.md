```python
import dataclasses
from typing import Literal

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
