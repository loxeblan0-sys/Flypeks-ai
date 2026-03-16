from typing import Literal

def agent_schedule_task(
    name: str,
    schedule_type: Literal["cron", "interval"],
    prompt: str,
    repeat: bool = False,
    cron_expression: str = None,
    interval_seconds: int = None
) -> dict:
    """Schedule a task to run at a specific time or interval.

    When to use:
    - When the user requests a task to be executed in the future
    - When the user requests a recurring task (e.g., daily, weekly)
    """
    # This tool registers a new job with the system-level scheduler service.
    # The scheduler will then trigger the AgentRuntime with the specified prompt
    # at the defined time or interval.
    return {
        "status": "task_scheduled",
        "job_name": name,
        "schedule": cron_expression if schedule_type == "cron" else f"every {interval_seconds}s",
        "repeat": repeat,
        "prompt": prompt
    }
