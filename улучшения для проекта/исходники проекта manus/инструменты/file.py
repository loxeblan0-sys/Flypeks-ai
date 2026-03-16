import dataclasses
from typing import Literal, List, Optional, Dict, Any

@dataclasses.dataclass(kw_only=True)
class FileEdits:
  find: str
  replace: str
  all: Optional[bool] = None

def file(
    brief: str,
    action: Literal["view", "read", "write", "append", "edit"],
    path: str,
    edits: Optional[List[FileEdits]] = None,
    range: Optional[List[int]] = None,
    text: Optional[str] = None,
) -> Dict[str, Any]:
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
  print(f"Simulating file tool call: brief=\\'{brief}\\' action={action}, path=\\'{path}\\' edits={edits}, range={range}, text=\\'{text[:50] if text else None}...\'")
  return {"status": "success", "tool": "file"}

# Example Usage:
if __name__ == "__main__":
    # Example 1: Write to a file
    file(
        brief="Create a new Python script",
        action="write",
        path="/home/ubuntu/my_script.py",
        text="print(\'Hello, Agent!\')\n"
    )
    # Example 2: Read from a file
    file(
        brief="Read existing script",
        action="read",
        path="/home/ubuntu/my_script.py"
    )
    # Example 3: Edit a file
    file(
        brief="Update script content",
        action="edit",
        path="/home/ubuntu/my_script.py",
        edits=[
            FileEdits(find="Hello", replace="Greetings"),
            FileEdits(find="Agent", replace="World", all=True)
        ]
    )
