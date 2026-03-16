# --- File: /tools/system/shell_tool.py ---

import subprocess
import os
from typing import Dict, Any, List

# Security Constants
DOCKER_IMAGE = "ubuntu:22.04"
DEFAULT_TIMEOUT = 60
MAX_TIMEOUT = 300
WORKSPACE_HOST_PATH = os.environ.get("AGENT_WORKSPACE_PATH", "/home/ubuntu")
WORKSPACE_CONTAINER_PATH = "/workspace"

class ShellTool:
    """
    Tool for safely executing shell commands in an isolated Docker environment.
    """

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method called by the `tool_dispatcher`.
        """
        command: str = arguments.get("command")
        timeout: int = arguments.get("timeout_seconds", DEFAULT_TIMEOUT)
        allowed_hosts: List[str] = arguments.get("allowed_network_hosts", [])

        # 1. Input Validation and Sanitization (Level 8)
        if not command or not isinstance(command, str):
            return self._format_error("Argument 'command' must be a non-empty string.")
        
        if timeout > MAX_TIMEOUT:
            timeout = MAX_TIMEOUT

        # 2. Build the Docker command (Level 2)
        docker_command = self._build_docker_command(allowed_hosts)

        # 3. Execution in a separate process with timeout
        try:
            process = subprocess.Popen(
                docker_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )

            # Pass the command into the container's STDIN
            stdout_data, stderr_data = process.communicate(input=command, timeout=timeout)
            
            exit_code = process.returncode

        except subprocess.TimeoutExpired:
            process.kill()
            stdout_data, stderr_data = process.communicate()
            return self._format_error(f"Command timed out after {timeout} seconds.", exit_code=-1)
        
        except Exception as e:
            return self._format_error(f"An unexpected error occurred: {str(e)}", exit_code=-1)

        # 4. Result Formatting (Level 4)
        return {
            "stdout": stdout_data,
            "stderr": stderr_data,
            "exit_code": exit_code
        }

    def _build_docker_command(self, allowed_hosts: List[str]) -> List[str]:
        """
        Assembles the arguments to run the Docker container.
        """
        # Base command with constraints
        cmd = [
            "docker", "run",
            "--rm",         # Automatically remove the container after execution
            "-i",           # Keep STDIN open for passing the command
            "--read-only",  # Image file system is read-only
            "--memory=512m",# Memory limit
            "--cpus=0.5",   # CPU limit
            f"--mount=type=bind,source={WORKSPACE_HOST_PATH},target={WORKSPACE_CONTAINER_PATH}",
            DOCKER_IMAGE,
            "/bin/bash"
        ]

        # Dynamic Network Control (Level 8 - Capability Guard)
        if not allowed_hosts:
            cmd.insert(2, "--network=none")
        else:
            # Complex logic for temporary network creation would go here.
            pass 

        return cmd

    def _format_error(self, error_message: str, exit_code: int = -1) -> Dict[str, Any]:
        """
        Wraps an error into a standard result format.
        """
        return {
            "stdout": "",
            "stderr": f"SHELL_TOOL_ERROR: {error_message}",
            "exit_code": exit_code
        }

# Instance for tool_dispatcher
shell_tool_instance = ShellTool()
