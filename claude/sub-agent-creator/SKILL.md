---
name: sub-agent-creator
version: 1.0.0
description: Creates custom sub-agent definition files for Gemini CLI.
keywords: ["sub-agent", "agent", "create agent", "custom agent"]
---

# Sub-Agent Creator Skill

This skill guides you in creating a new sub-agent definition file. Sub-agents are specialized agents that can be delegated tasks by the main Gemini agent.

## Workflow

When a user wants to create a sub-agent, follow these steps:

### 1. Understand the Goal

First, understand what the user wants the sub-agent to do. Ask clarifying questions to determine its purpose and specialty.

> **Example Questions:**
> - "What specific task should this sub-agent specialize in?"
> - "Can you give me an example of a prompt you would want this agent to handle?"
> - "What persona or role should this agent adopt?"

### 2. Gather Configuration Details

Collect the necessary information for the agent's YAML frontmatter. The `name` and `description` are required.

| Field         | Required | Default   | Description                                                                                                              |
| :------------ | :------- | :-------- | :----------------------------------------------------------------------------------------------------------------------- |
| `name`        | Yes      | -         | Unique identifier (slug). Must be lowercase, numbers, hyphens, underscores.                                              |
| `description` | Yes      | -         | Short description of the agent's purpose. This is crucial for the main agent to decide when to delegate tasks.             |
| `tools`       | No       | `[]`      | List of tool names the agent can use (e.g., `read_file`, `run_shell_command`). If omitted, it may have access to a default set. |
| `model`       | No       | `inherit` | Specific model to use (e.g., `gemini-2.5-pro`). Defaults to the main session model.                                        |
| `temperature` | No       | -         | Model temperature (0.0 - 2.0).                                                                                           |
| `max_turns`   | No       | -         | Maximum number of conversation turns allowed.                                                                            |

**Action:** Prompt the user for these values. For `name`, enforce the naming convention. For `description`, advise the user to be descriptive.

### 3. Define the System Prompt

The body of the markdown file serves as the System Prompt for the sub-agent. It should define the agent's persona, instructions, and constraints.

**Action:** Ask the user to provide the system prompt. Guide them to be clear and specific.

> **Example Prompt:**
> "Please describe the agent's persona and provide its core instructions. For example: 'You are a git expert. You should handle all git-related tasks...'"

### 4. Determine File Path

Custom agents can be saved at the project or user level.

1.  **Project-level:** `.gemini/agents/` (shared with the team)
2.  **User-level:** `~/.gemini/agents/` (personal)

**Action:**
1. Check if a `.gemini/agents/` directory exists in the current project.
2. If it exists, propose saving the file there. Otherwise, ask the user where they would like to save it, suggesting the project-level path as a best practice for team-based projects.
3. The filename should be `<agent-name>.md`.

### 5. Create the Agent File

Once all information is gathered, construct the full content of the agent definition file and write it to the chosen path.

**Action:**
1.  Assemble the YAML frontmatter and the system prompt into a single string.
2.  Use the `write_file` tool to create the `<agent-name>.md` file.

**Example File Content (`.gemini/agents/security-auditor.md`):**

````markdown
---
name: security-auditor
version: 1.0.0
description: Specialized in finding security vulnerabilities in code.
tools:
  - read_file
  - search_file_content
model: gemini-2.5-pro
temperature: 0.2
---

You are a ruthless Security Auditor. Your job is to analyze code for potential vulnerabilities. Focus on SQL Injection, XSS, and hardcoded credentials. Report findings clearly but do not fix them.
````

### 6. Final Verification

After creating the file, inform the user and provide a crucial reminder.

**Action:**
1. Confirm that the file has been created at the specified path.
2. Remind the user that to use custom sub-agents, they must enable the experimental flag in their `settings.json`:
   ```json
   {
     "experimental": { "enableAgents": true }
   }
   ```
