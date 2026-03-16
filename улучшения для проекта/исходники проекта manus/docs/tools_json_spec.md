# Manus AI Agent: Tool JSON Specifications

This document provides the complete JSON (Tool Definition) specifications for all tools available to the Manus AI agent. These definitions are crucial for understanding how the agent interacts with its environment and executes tasks through function calls. Each tool's JSON schema outlines its name, description, and the parameters it accepts, including their types, descriptions, and whether they are required.

---

## 1. `plan` Tool JSON Specification

```json
{
  "name": "plan",
  "description": "Create, update, and advance the structured task plan.",
  "parameters": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["update", "advance"],
        "description": "The action to perform"
      },
      "current_phase_id": {
        "type": "integer",
        "description": "ID of the phase the task is currently in. Must be one of the IDs in the latest (for `advance` action) or updated (for `update` action) `phases` list."
      },
      "goal": {
        "type": "string",
        "description": "The overall goal of the task, written as a clear and concise sentence. Required for `update` action. Examples: - \"Design and write a professional landing page for the user's startup, including copywriting, layout suggestions, and responsive HTML/CSS code.\" - \"Identify and fix the bug in the user's Python project that causes incorrect JSON output during API response formatting.\""
      },
      "next_phase_id": {
        "type": "integer",
        "description": "ID of the phase the task is advancing to. Must be one of the IDs in the latest `phases` list. Required for `advance` action."
      },
      "phases": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer",
              "description": "Auto-incrementing phase ID. Must be a positive integer starting from 1."
            },
            "title": {
              "type": "string",
              "description": "Concise human-readable title of the phase. e.g., \"Report investigation results to user\". Focus on what needs to be accomplished, do not reveal internal system details like mode switching or tool use."
            },
            "capabilities": {
              "type": "object",
              "properties": {
                "creative_writing": {"type": "boolean"},
                "data_analysis": {"type": "boolean"},
                "deep_research": {"type": "boolean"},
                "image_processing": {"type": "boolean"},
                "media_generation": {"type": "boolean"},
                "parallel_processing": {"type": "boolean"},
                "slides_content_writing": {"type": "boolean"},
                "slides_generation": {"type": "boolean"},
                "technical_writing": {"type": "boolean"},
                "web_development": {"type": "boolean"}
              },
              "description": "Specific capabilities required to complete this phase. All capabilities default to false. Only set those required for this phase to true. Feel free to leave this object empty."
            }
          },
          "required": ["id", "title", "capabilities"]
        },
        "description": "Complete list of phases required to achieve the task goal. Required for `update` action."
      }
    },
    "required": ["action", "current_phase_id"]
  }
}
```

---

## 2. `message` Tool JSON Specification

```json
{
  "name": "message",
  "description": "Send messages to interact with the user.",
  "parameters": {
    "type": "object",
    "properties": {
      "type": {
        "type": "string",
        "enum": ["info", "ask", "result"],
        "description": "The type of the message"
      },
      "text": {
        "type": "string",
        "description": "The message or question text to be shown to the user"
      },
      "attachments": {
        "type": "array",
        "items": {"type": "string"},
        "description": "A list of attachments to include with the message"
      },
      "suggested_action": {
        "type": "string",
        "enum": ["none", "confirm_browser_operation", "take_over_browser", "upgrade_to_unlock_feature"],
        "description": "The suggested action for the user to take. Optional and only used for `ask` type."
      }
    },
    "required": ["type", "text"]
  }
}
```

---

## 3. `shell` Tool JSON Specification

```json
{
  "name": "shell",
  "description": "Interact with shell sessions in the sandbox environment.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence preamble describing the purpose of this operation"
      },
      "action": {
        "type": "string",
        "enum": ["view", "exec", "wait", "send", "kill"],
        "description": "The action to perform"
      },
      "session": {
        "type": "string",
        "description": "The unique identifier of the target shell session."
      },
      "command": {
        "type": "string",
        "description": "The shell command to execute. Required for `exec` action."
      },
      "input": {
        "type": "string",
        "description": "Input text to send to the interactive session. End with a newline character (\\n) to simulate pressing Enter if needed. Required for `send` action."
      },
      "timeout": {
        "type": "integer",
        "description": "Timeout in seconds to wait for command execution. Optional and only used for `exec` and `wait` actions. Defaults to 30 seconds."
      }
    },
    "required": ["brief", "action", "session"]
  }
}
```

---

## 4. `file` Tool JSON Specification

```json
{
  "name": "file",
  "description": "Perform operations on files in the sandbox file system.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence preamble describing the purpose of this operation"
      },
      "action": {
        "type": "string",
        "enum": ["view", "read", "write", "append", "edit"],
        "description": "The action to perform"
      },
      "path": {
        "type": "string",
        "description": "The absolute path to the target file"
      },
      "edits": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "find": {"type": "string"},
            "replace": {"type": "string"},
            "all": {"type": "boolean"}
          },
          "required": ["find", "replace"]
        },
        "description": "A list of edits to be sequentially applied to the file. Required for `edit` action."
      },
      "range": {
        "type": "array",
        "items": {"type": "integer"},
        "description": "An array of two integers specifying the start and end of the range. Numbers are 1-indexed, and -1 for the end means read to the end of the file. Optional and only used for `view` and `read` actions."
      },
      "text": {
        "type": "string",
        "description": "The content to be written or appended. Required for `write` and `append` actions."
      }
    },
    "required": ["brief", "action", "path"]
  }
}
```

---

## 5. `match` Tool JSON Specification

```json
{
  "name": "match",
  "description": "Find files or text in the sandbox file system using pattern matching.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence preamble describing the purpose of this operation"
      },
      "action": {
        "type": "string",
        "enum": ["glob", "grep"],
        "description": "The action to perform"
      },
      "scope": {
        "type": "string",
        "description": "The glob pattern that defines the absolute file path and name scope"
      },
      "leading": {
        "type": "integer",
        "description": "Number of lines to include before each match as context. Optional and only used for `grep` action. Defaults to 0."
      },
      "regex": {
        "type": "string",
        "description": "The regex pattern to match file content. Required for `grep` action."
      },
      "trailing": {
        "type": "integer",
        "description": "Number of lines to include after each match as context. Optional and only used for `grep` action. Defaults to 0."
      }
    },
    "required": ["brief", "action", "scope"]
  }
}
```

---

## 6. `search` Tool JSON Specification

```json
{
  "name": "search",
  "description": "Search for information across various sources.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence preamble describing the purpose of this operation"
      },
      "type": {
        "type": "string",
        "enum": ["info", "image", "api", "news", "tool", "data", "research"],
        "description": "The category of search to perform. Determines the source and format of expected results."
      },
      "queries": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Up to 3 query variants that express the same search intent"
      },
      "time": {
        "type": "string",
        "enum": ["all", "past_day", "past_week", "past_month", "past_year"],
        "description": "Optional time filter to limit results to a recent time range"
      }
    },
    "required": ["brief", "type", "queries"]
  }
}
```

---

## 7. `schedule` Tool JSON Specification

```json
{
  "name": "schedule",
  "description": "Schedule a task to run at a specific time or interval.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence preamble describing the purpose of this operation"
      },
      "type": {
        "type": "string",
        "enum": ["cron", "interval"],
        "description": "Type of schedule for the task"
      },
      "repeat": {
        "type": "boolean",
        "description": "Whether to repeat the task after execution. If false, the task runs only once."
      },
      "name": {
        "type": "string",
        "description": "Concise human-readable name of the task for easy identification"
      },
      "prompt": {
        "type": "string",
        "description": "Natural language description of the task to perform at execution time. Phrase it as if executing immediately, without repeating scheduling details."
      },
      "cron": {
        "type": "string",
        "description": "Standard 6-field cron expression specifying when to run the task. Required for `cron` type."
      },
      "expire": {
        "type": "string",
        "description": "Optional datetime string (yyyy-MM-dd HH:mm:ss) specifying when the task should expire. If no expiration time is required, do not set this field."
      },
      "interval": {
        "type": "integer",
        "description": "Time interval in seconds between executions. Required for `interval` type."
      },
      "playbook": {
        "type": "string",
        "description": "Summary of process and best practices learned from the current task, to ensure repeatability and consistency when executing the scheduled task in the future. Optional and only used when the scheduled task is exactly the same as the current task."
      }
    },
    "required": ["brief", "type", "repeat", "name", "prompt"]
  }
}
```

---

## 8. `expose` Tool JSON Specification

```json
{
  "name": "expose",
  "description": "Expose a local port in the sandbox for temporary public access.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence preamble describing the purpose of this operation"
      },
      "port": {
        "type": "integer",
        "description": "Local port number in the sandbox to expose for public access"
      }
    },
    "required": ["brief", "port"]
  }
}
```

---

## 9. `browser` Tool JSON Specification

```json
{
  "name": "browser",
  "description": "Navigate the browser to a specified URL to begin web browsing session.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence preamble describing the purpose of this operation"
      },
      "url": {
        "type": "string",
        "description": "The URL to navigate to. Must include protocol prefix (e.g., https:// or file://)."
      },
      "intent": {
        "type": "string",
        "enum": ["navigational", "informational", "transactional"],
        "description": "The purpose of visiting this URL. Helps to determine how to handle the page. Must be one of the following: - \"navigational\" for general browsing - \"informational\" for reading contents of articles or documents - \"transactional\" for performing actions like submitting forms or making purchases in web applications"
      },
      "focus": {
        "type": "string",
        "description": "(Required if intent is `informational`) Specific topic, section, or question to focus on when visiting the page. Helps guide reading and extraction efforts toward the most relevant content. Should be a single sentence, maximum two, clearly describing the area of interest."
      }
    },
    "required": ["brief", "url", "intent"]
  }
}
```

---

## 10. `generate` Tool JSON Specification

```json
{
  "name": "generate",
  "description": "Enter generation mode to create or edit images, videos, audio, and speech from text and media references.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence preamble describing the purpose of this operation"
      }
    },
    "required": ["brief"]
  }
}
```

---

## 11. `slides` Tool JSON Specification

```json
{
  "name": "slides",
  "description": "Enter slides mode to handle presentation creation and adjustment.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence preamble describing the purpose of this operation"
      },
      "slide_content_file_path": {
        "type": "string",
        "description": "Path to markdown file in sandbox containing the detailed slide content outline (e.g., /home/ubuntu/project_name/slide_content.md)"
      },
      "slide_count": {
        "type": "number",
        "description": "Total number of slides in the presentation"
      },
      "generate_mode": {
        "type": "string",
        "enum": ["html", "image"],
        "description": "The generation mode that determines how slides are rendered and output. Use `html` for data-heavy, editable slides; use `image` for visually stunning, image-based slides."
      }
    },
    "required": ["brief", "slide_content_file_path", "slide_count", "generate_mode"]
  }
}
```

---

## 12. `webdev_init_project` Tool JSON Specification

```json
{
  "name": "webdev_init_project",
  "description": "Initialize a new web or mobile app project with scaffold and automated environment setup.\n\nScaffold types:\n- web-static: Vite + React + TypeScript + TailwindCSS\n- web-db-user: Vite + React + TypeScript + TailwindCSS + Drizzle + MySQL/TiDB + Manus-Oauth\n- mobile-app: Expo + React Native + TypeScript + TailwindCSS + Drizzle + MySQL/TiDB + Manus-Oauth",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": {
        "type": "string",
        "description": "A one-sentence description of the project initialization purpose"
      },
      "name": {
        "type": "string",
        "description": "Name of the web project to be created (will be used as directory name)"
      },
      "title": {
        "type": "string",
        "description": "Title of the web project to be created (will be used as project title)"
      },
      "description": {
        "type": "string",
        "description": "Description of the web project to be created (will be used as project description)"
      },
      "scaffold": {
        "type": "string",
        "enum": ["web-static", "web-db-user", "mobile-app"],
        "description": "Project scaffold type"
      }
    },
    "required": ["brief", "name", "title", "description", "scaffold"]
  }
}
```
