from typing import Literal, Optional, Dict, Any, List

def schedule(
    brief: str,
    type: Literal["cron", "interval"],
    repeat: bool,
    name: str,
    prompt: str,
    cron: Optional[str] = None,
    expire: Optional[str] = None,
    interval: Optional[int] = None,
    playbook: Optional[str] = None,
) -> Dict[str, Any]:
  """Schedule a task to run at a specific time or interval.

  <supported_types>
  - `cron`: Schedule based on cron expression for precise timing control
  - `interval`: Schedule based on time intervals for simple recurring tasks
  </supported_types>

  <instructions>
  - This tool is primarily for scheduling task execution, not for setting reminders or alarms
  - For reminders or alarms, prioritize calendar/reminder tools or MCP servers if available
  - Only one scheduled task can exist at a time; the first call creates it, and subsequent calls modify the existing task
  - Execution of `cron` tasks is based on the user\"s timezone
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
  - Use commas to specify multiple values in a field, e.g. \"0 0 12 * * 1,3,5\" (Monday, Wednesday, Friday at noon)
  - Use hyphens to specify ranges, e.g. \"0 0 9-17 * * 1-5\" (Weekdays 9am to 5pm)
  - Use slashes to specify step values, e.g. \"0 */15 * * * *\" (Every 15 minutes)
  - Combine these patterns to create complex schedules, e.g. \"0 0 9,13,17 * * 1-5\" (Weekdays at 9am, 1pm, and 5pm)
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
  print(f"Simulating schedule tool call: brief=\"{brief}\", type={type}, repeat={repeat}, name=\"{name}\", prompt=\"{prompt[:50]}...\", cron=\"{cron}\", expire=\"{expire}\", interval={interval}")
  return {"status": "success", "tool": "schedule"}

# Example Usage:
if __name__ == "__main__":
    schedule(
        brief="Schedule daily report generation",
        type="cron",
        repeat=True,
        name="DailyReport",
        prompt="Generate and send daily performance report.",
        cron="0 0 9 * * *" # Every day at 9 AM
    )
    schedule(
        brief="Run task in 5 minutes",
        type="interval",
        repeat=False,
        name="DelayedTask",
        prompt="Perform a quick system check.",
        interval=300 # 5 minutes
    )
