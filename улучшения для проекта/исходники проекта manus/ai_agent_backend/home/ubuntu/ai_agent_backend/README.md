# AI Agent Backend Prototype

This project is a prototype of an autonomous AI agent backend, inspired by the architecture of systems like Manus. It uses an LLM (Large Language Model) with tool-calling capabilities to perform tasks in a sandboxed environment.

## Features

- **Modular Architecture**: Core logic is separated into an Orchestrator, ToolManager, and Sandbox.
- **Tool System**: Easily extensible system for adding new tools (functions) for the agent to use.
- **Secure Execution**: A conceptual sandbox for executing commands and file operations safely.
- **Disclosure Prohibition**: A mechanism to prevent the agent from revealing its internal system prompts.

## Project Structure

```
ai_agent_backend/
├── core/
│   ├── agent.py         # Core AgentOrchestrator logic
│   ├── prompts.py       # System prompts and security rules
│   ├── sandbox.py       # Sandbox environment for secure execution
│   └── tools.py         # Tool registration and management
├── tools/
│   ├── shell_tool.py    # Example shell tool implementation
│   └── file_tool.py     # Example file tool implementation
├── main.py            # Main entrypoint
└── README.md          # This file
```

## Setup and Installation

1.  **Prerequisites**:
    *   Python 3.9+
    *   An OpenAI API key (or another LLM provider that supports tool calling).

2.  **Installation**:
    *   Clone this repository.
    *   Install the required Python packages:
        ```bash
        pip install openai
        ```

3.  **Configuration**:
    *   Set your OpenAI API key as an environment variable:
        ```bash
        export OPENAI_API_KEY=\'your_api_key_here\'
        ```

## How to Run

1.  Navigate to the `ai_agent_backend` directory.
2.  Run the main script:
    ```bash
    python main.py
    ```
3.  You will see a `User >` prompt. Type your requests to the agent and press Enter.
4.  Type `exit` to quit the application.

## How It Works

1.  The `main.py` script initializes all components: the Sandbox, the ToolManager (with all available tools), the MemoryModule (with system prompts), and finally the `AgentOrchestrator`.
2.  When you type a request, the `AgentOrchestrator` begins its main loop.
3.  It constructs a detailed prompt containing system instructions, tool definitions, and the conversation history, then sends it to the LLM.
4.  The LLM decides whether to call a tool or respond with text.
5.  If a tool is called, the `ToolManager` executes it via the `Sandbox`.
6.  The result of the tool execution is added to the conversation history.
7.  The loop repeats, sending the updated context back to the LLM until the task is complete and the LLM generates a final text response.

## Disclaimer

This is a conceptual prototype. The sandbox implementation is basic and does not provide the level of security required for a production environment. For a real-world application, use containerization technologies like Docker for true isolation.
