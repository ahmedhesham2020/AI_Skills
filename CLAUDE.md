# AI Skills Library — Automation Rules

## Dual-Format Skill Rule (ALWAYS apply)

When creating or updating ANY skill in this repository, you MUST maintain two versions:

| Folder | CLI | Format rules |
|--------|-----|-------------|
| `claude/[skill-name]/` | Claude Code (`claude` CLI) | Keep `version:` in frontmatter, keep `$ARGUMENTS`, keep explicit tool references (`Write tool`, `Bash tool`, etc.) |
| `gemini/[skill-name]/` | Gemini CLI (`gemini` CLI) | Remove `version:` from frontmatter, remove `$ARGUMENTS` line, replace explicit tool refs with natural language |

### Transformation rules for Gemini version

When writing the Gemini version of any skill, apply these substitutions to the Claude version:

- Remove `version: x.x.x` from frontmatter
- Remove `**ARGUMENTS: $ARGUMENTS**` line
- `Parse \`$ARGUMENTS\`` → `Parse the user's request`
- `from \`$ARGUMENTS\`` → `from the user's request`
- `Extract from \`$ARGUMENTS\`` → `Extract from the user's request`
- `$ARGUMENTS` (any remaining) → `the user's request`
- `Use the Write tool to` → `Write a file named`
- `using the Write tool` → `(write this to disk)`
- `Use the Bash tool to run` → `Run the command`
- `Use the Bash tool to` → `Run`
- `Use the Read tool to` → `Read`
- `Use the Grep tool to` → `Search for`

### Workflow for new skills

1. Write the full skill in `claude/[skill-name]/SKILL.md`
2. Apply the transformation rules above to produce `gemini/[skill-name]/SKILL.md`
3. Copy any `references/` folder into both `claude/[skill-name]/references/` and `gemini/[skill-name]/references/`
4. The root-level skill folders (e.g. `capl-script-generator/` at repo root) are the **Claude version** — keep them in sync with `claude/[skill-name]/`
5. Update the README.md to reflect any new skill added

### Installation paths

- **Claude Code:** `~/.claude/skills/` — symlink or copy the `claude/` folder contents
- **Gemini CLI:** `~/.gemini/skills/` or `~/.agents/skills/` — symlink or copy the `gemini/` folder contents
