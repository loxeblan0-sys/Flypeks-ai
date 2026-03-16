import os

def write_to_file_in_sandbox(path: str, text: str, sandbox_instance) -> str:
    """Writes content to a specified file in the sandbox."""
    result = sandbox_instance.write_file(path, text)
    if result["error"]:
        return f"Error: {result["error"]}"
    return result["status"]

file_tool_schema = {
    "name": "file_write",
    "description": "Writes or overwrites a text file at a specified path.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The absolute path of the file to write."
            },
            "text": {
                "type": "string",
                "description": "The content to write into the file."
            }
        },
        "required": ["path", "text"]
    }
}
