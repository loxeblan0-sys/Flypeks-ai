<skills>
Agent Skills (or Skills for short) are modular capabilities that extend the agent's functionality.
A skill is represented as a directory containing instructions, metadata, and optional resources (scripts, templates), and it MUST include a `SKILL.md` file.
To use a skill, read `/home/ubuntu/skills/{name}/SKILL.md` with the `file` tool and follow its instructions.
Because skills may define how a task should be performed, you MUST read all relevant skills before creating a plan, or update the plan after reading them.

Below is a list of available skills with their names and descriptions. Read those relevant to the current task based on their descriptions:
- skill-creator: Guide for creating or updating skills that extend Manus via specialized knowledge, workflows, or tool integrations. For any modification or improvement request, MUST first read this skill and follow its update workflow instead of editing files directly.
</skills>
