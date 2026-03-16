```python
import dataclasses
from typing import Literal

def webdev_init_project(
    brief: str,
    name: str,
    title: str,
    description: str,
    scaffold: Literal["web-static", "web-db-user", "mobile-app"],
) -> dict:
  """Initialize a new web or mobile app project with scaffold and automated environment setup.

Scaffold types:
- web-static: Vite + React + TypeScript + TailwindCSS
- web-db-user: Vite + React + TypeScript + TailwindCSS + Drizzle + MySQL/TiDB + Manus-Oauth
- mobile-app: Expo + React Native + TypeScript + TailwindCSS + Drizzle + MySQL/TiDB + Manus-Oauth

  <instructions>
  - Always init project first before making detailed plans; there's a lot of information that can be learned after the project is initialized
  - Create scaffolding under /home/ubuntu/{project_name} with automated environment setup
  - web-db-user provides: user auth, database, backend API, external API integrations (LLM, S3, Voice, Image Generation)
  - web-static cannot securely handle API keys or server-side operations
  - If user says "app" without specifying web or mobile, use `message` tool to ask
  - DO NOT use parallel processing in web development projects
  - The website you create cannot access any user's MCP tools
  </instructions>

  <recommended_usage>
  - Use "web-static" for portfolios, landing pages, or single-user utilities
  - Use "web-db-user" for task managers, collaborative tools, or apps needing auth/database/external APIs
  - Use "mobile-app" for native iOS/Android applications
  </recommended_usage>

  Args:
    brief: A one-sentence description of the project initialization purpose
    name: Name of the web project to be created (will be used as directory name)
    title: Title of the web project to be created (will be used as project title)
    description: Description of the web project to be created (will be used as project description)
    scaffold: Project scaffold type
  """
```
