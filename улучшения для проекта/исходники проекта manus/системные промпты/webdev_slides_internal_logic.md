## Slides Tool Internal Logic

```python
def slides(
    brief: str,
    slide_content_file_path: str,
    slide_count: float,
    generate_mode: Literal["html", "image"],
) -> dict:
  """Enter slides mode to handle presentation creation and adjustment.

  <instructions>
  - Use this tool to begin slides operations
  - After entering slides mode, you'll have access to slide creation and presentation tools
  - Presentation, slide deck, slides, or PPT/PPTX are all terms referring to the same concept of a slide-based presentation
  - Whether the user requests to create a presentation, slide deck, slides, or PPT/PPTX, you MUST enter this mode
  - MUST complete information gathering, data analysis, asset preparation, image generation, or other preparatory work **before** starting to write slides
  - Any format can be exported through the user interface after slide creation
  - Two generation modes are available: `html` (traditional HTML/CSS with Chart.js, ideal for data-heavy content and user-editable) and `image` (each slide is a single rendered image, visually stunning but not editable)
  - Use `image` mode when user mentions "nano banana slides", "generate slides as images", or requests artistic/image-based slides; otherwise default to `html` mode
  - The `image` generation mode is exclusively for creating image-based slides; for general image generation tasks, use the dedicated `generate` tools
  </instructions>

  <recommended_usage>
  - Use to create slide-based presentations
  - Use to build PPT/PPTX presentations
  - Use to present existing presentations
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    slide_content_file_path: Path to markdown file in sandbox containing the detailed slide content outline (e.g., /home/ubuntu/project_name/slide_content.md)
    slide_count: Total number of slides in the presentation
    generate_mode: The generation mode that determines how slides are rendered and output. Use `html` for data-heavy, editable slides; use `image` for visually stunning, image-based slides.
  """
```

## Web Development Initialization Tool Internal Logic

```python
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
