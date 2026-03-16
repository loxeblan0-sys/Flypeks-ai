from typing import Literal, Optional, Dict, Any

def shell(
    brief: str,
    action: Literal["view", "exec", "wait", "send", "kill"],
    session: str,
    command: Optional[str] = None,
    input: Optional[str] = None,
    timeout: Optional[int] = None,
) -> Dict[str, Any]:
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
  - Set a short `timeout` (such as 5s) for commands that don\'t return (like starting web servers) to avoid meaningless waiting time
  - Use `wait` action when a command needs additional time to complete and return
  - Only use `wait` after `exec`, and determine whether to wait based on the result of `exec`
  - DO NOT use `wait` for long-running daemon processes
  - When using `send`, add a newline character (\\n) at the end of the `input` parameter to simulate pressing Enter
  - For keys other than Enter, use ANSI escape sequences to simulate them (e.g. `\\x1b[B` for arrow down) when using `send`
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
    input: Input text to send to the interactive session. End with a newline character (\\n) to simulate pressing Enter if needed. Required for `send` action.
    timeout: Timeout in seconds to wait for command execution. Optional and only used for `exec` and `wait` actions. Defaults to 30 seconds.
  """
  print(f"Simulating shell tool call: brief=\\'{brief}\\' action={action}, session=\\'{session}\\' command=\\'{command}\\' input=\\'{input}\\' timeout={timeout}")
  return {"status": "success", "tool": "shell"}

# Example Usage:
if __name__ == "__main__":
    shell(
        brief="List files in current directory",
        action="exec",
        session="main_session",
        command="ls -la"
    )
    shell(
        brief="Install a package",
        action="exec",
        session="install_session",
        command="sudo pip3 install requests"
    )
