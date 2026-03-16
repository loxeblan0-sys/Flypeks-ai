
# Manus-like AI Agent: UX for Chat Modes and Template Selection

This document details the user experience (UX) and user interface (UI) design for managing different operational modes within an AI agent's chat interface, specifically focusing on how users select modes and are presented with project templates (scaffolds). The goal is to replicate the intuitive and context-aware interaction patterns found in advanced AI platforms like Manus.

## 1. Dynamic Mode Switching in Chat

The agent's chat interface should intelligently adapt to the user's intent, offering specific tools and workflows based on the current context or explicit user commands. This can be achieved through a combination of implicit and explicit mode switching.

### 1.1. Implicit Mode Detection

*   **Contextual Keywords**: The agent's LLM continuously analyzes user input for keywords or phrases that indicate a shift in intent (e.g., "create a website", "build a presentation", "generate an image").
*   **Tool Call Trigger**: When the LLM decides to use a mode-specific tool (e.g., `webdev_init_project`, `slides`, `generate`), the UI should reflect this mode activation.

### 1.2. Explicit Mode Selection (UI Elements)

To provide users with direct control and visibility, dedicated UI elements for mode selection are crucial.

*   **Persistent Mode Selector**: A set of buttons or a dropdown menu, possibly located in a sidebar or a dedicated header section, allowing users to explicitly switch between major modes (e.g., "Chat", "WebDev", "Slides", "Media Generation").
    *   **Visual Feedback**: The currently active mode should be clearly highlighted.
    *   **Mode-Specific Prompts**: When a mode is selected, the chat input area's placeholder text might change (e.g., "Describe your website idea..." in WebDev mode, "Outline your presentation..." in Slides mode).
*   **Contextual Quick Actions**: Small, floating buttons or a quick-access menu that appears near the chat input when the agent detects a potential mode switch. For example, if the user mentions "website", a small button "Start Web Project" could appear.

### 1.3. Mode-Specific Chat Experience

Once a mode is active, the chat interface should tailor its behavior:

*   **Relevant Tool Suggestions**: The agent should prioritize suggesting and executing tools relevant to the active mode.
*   **Mode-Specific Information Display**: Outputs from tools within that mode (e.g., `webdev_init_project` output, `slides` generation progress) should be prominently displayed.
*   **Persistent Context**: The agent should maintain the context of the active mode, even if the user briefly switches to general chat for a question, and seamlessly return to the mode's workflow.

## 2. Dynamic Template Suggestion and Selection

After a user enters a project-oriented mode (e.g., WebDev, Slides), the system should proactively offer relevant templates (scaffolds) to streamline the creation process.

### 2.1. Template Suggestion UI

*   **Bottom-of-Chat Carousel/List**: A prominent area at the bottom of the chat window (above the input field) should display a carousel or a list of suggested templates.
    *   **Visual Cards**: Each template should be represented by a visually appealing card containing:
        *   **Template Name**: (e.g., "Static Website", "Blog with Database", "Mobile App")
        *   **Brief Description**: A one-sentence summary of what the template provides.
        *   **Key Technologies**: Icons or text indicating the tech stack (e.g., React, Vite, Tailwind, Drizzle).
        *   **"Select" Button**: To choose this template.
        *   **"Preview" Button (Optional)**: To view a live demo or screenshot of the template.
*   **Contextual Filtering**: The suggested templates should be filtered based on the active mode. For instance, in "WebDev" mode, only web-related scaffolds should appear. If the user's initial prompt was specific (e.g., "I need a blog"), the agent might highlight or pre-select a relevant template.

### 2.2. Template Selection Flow

1.  **User Clicks "Select"**: When a user chooses a template, the agent should acknowledge the selection.
2.  **Project Details Form**: A small, inline form or a modal should appear, prompting the user for essential project details:
    *   **Project Name**: (e.g., `my-new-website`)
    *   **Project Title**: (e.g., "My Awesome Website")
    *   **Project Description**: A brief overview.
    *   **"Create Project" Button**: Initiates the `webdev_init_project` or `slides` tool call with the selected template and provided details.
    *   **"Back"/"Cancel" Button**: To return to template selection or cancel the operation.
3.  **Agent Execution Feedback**: Once "Create Project" is clicked, the UI should transition to showing the agent's execution of the `webdev_init_project` or `slides` tool, including progress indicators and logs, as described in the "Ultimate Agent Platform Blueprint".

## 3. Original Scaffolds (Templates) Structure

To provide the actual templates, we need to define their structure. These are the base files that the `webdev_init_project` tool would clone and modify. For simplicity, I will outline the core structure for a few common types. The actual files would reside in a designated `scaffolds/` directory on the agent's system.

### 3.1. `web-static` Scaffold (Vite + React + TypeScript + TailwindCSS)

This scaffold provides a modern, fast, and highly customizable frontend development setup.

```
scaffolds/web-static/
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   │   └── react.svg
│   ├── App.css
│   ├── App.tsx
│   ├── index.css
│   ├── main.tsx
│   └── vite-env.d.ts
├── .gitignore
├── index.html
├── package.json
├── postcss.config.js
├── README.md
├── tailwind.config.js
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

**Key Files and Their Purpose**:
*   `index.html`: The main entry point of the application. The agent would update the `<title>` tag and potentially inject a `<meta name="description">`.
*   `package.json`: Defines project metadata and dependencies. The agent would update `name`, `version`, `description`.
*   `src/App.tsx`: The main React component. Contains a basic "Hello World" setup.
*   `tailwind.config.js`, `postcss.config.js`: Tailwind CSS configuration files.
*   `vite.config.ts`: Vite build tool configuration.

### 3.2. `web-db-user` Scaffold (Vite + React + TypeScript + TailwindCSS + Drizzle + MySQL/TiDB + Manus-Oauth)

This scaffold extends the `web-static` with a backend, database integration, and user authentication. It would typically be a monorepo structure.

```
scaffolds/web-db-user/
├── frontend/ (similar to web-static scaffold)
│   ├── public/
│   ├── src/
│   ├── ...
│   └── package.json
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   └── auth.ts
│   │   │   └── users.ts
│   │   ├── db/
│   │   │   ├── schema.ts
│   │   │   └── drizzle.config.ts
│   │   ├── index.ts
│   │   └── types.ts
│   ├── .env.example
│   ├── package.json
│   ├── tsconfig.json
│   └── ... (e.g., Dockerfile, server config)
├── .gitignore
├── package.json (root monorepo package.json)
├── README.md
└── ... (e.g., Docker Compose for local DB)
```

**Key Files and Their Purpose**:
*   `frontend/`: Contains the client-side application, similar to `web-static`.
*   `backend/src/index.ts`: Main backend entry point, setting up an Express/Fastify server.
*   `backend/src/api/auth.ts`: Authentication routes and logic, integrated with Manus-Oauth.
*   `backend/src/db/schema.ts`: Drizzle ORM schema definitions for database tables (users, sessions, etc.).
*   `backend/.env.example`: Example environment variables for database connection, API keys, etc.
*   Root `package.json`: Manages monorepo workspaces and scripts.

### 3.3. `mobile-app` Scaffold (Expo + React Native + TypeScript + TailwindCSS + Drizzle + MySQL/TiDB + Manus-Oauth)

This scaffold provides a cross-platform mobile application setup.

```
scaffolds/mobile-app/
├── assets/
│   ├── adaptive-icon.png
│   └── favicon.png
├── components/
│   └── ... (e.g., Button.tsx, TextInput.tsx)
├── screens/
│   ├── HomeScreen.tsx
│   └── LoginScreen.tsx
├── App.tsx
├── app.json
├── babel.config.js
├── .env.example
├── .gitignore
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── ... (e.g., backend folder if monorepo)
```

**Key Files and Their Purpose**:
*   `App.tsx`: Main React Native component, setting up navigation and initial screen.
*   `app.json`: Expo configuration file, including app name, icon, splash screen.
*   `screens/`: Directory for different application screens.
*   `components/`: Reusable UI components.
*   `package.json`: Defines mobile app dependencies and scripts.
*   `tailwind.config.js`: Tailwind CSS configuration for React Native.

These scaffolds provide a solid starting point for various project types, allowing the agent to quickly set up a functional environment based on user selection. The agent's `webdev_init_project` tool would then take these base files, apply project-specific details (name, title, description), and install dependencies to create a ready-to-develop project directory.
