---
name: project-tracker
version: 1.0.0
description: >
  Use this skill when the user says "/project-tracker", "resume my project",
  "continue my project", "where did I leave off", "what's my next step",
  "pick up where we stopped", or provides a path to a markdown project tracking
  file and asks to continue. Also triggers when the user opens a new session
  and says something like "let's keep working" or "what was I doing last time"
  without specifying a project — check the default tracking file automatically.
---

**ARGUMENTS: $ARGUMENTS**

# Project Tracker Skill

## Purpose

Resume and drive forward any software project tracked in a markdown file.
The user should never have to paste a status prompt manually — this skill reads
the file, orients itself, and picks up exactly where the last session ended.

---

## Step 1 — Resolve the tracking file path

Parse `$ARGUMENTS` for a file path argument.

- If a path is provided, use it.
- If no path is provided, use the default:
  `/Users/ahmedhesham/Downloads/01-My Work/QA_Portfolio_Projects.md`

Use the Read tool to read the full file. If the file does not exist, tell the
user clearly and stop — do not guess or create a new file.

---

## Step 2 — Find the active project

Scan the file for projects in this priority order:

1. **First project with status `[~] In Progress`** — this is the active project.
2. If no `[~]` project exists, **first project with status `[ ] Not Started`** — start this one.
3. If all projects are `[x] Done`, congratulate the user and show the GitHub portfolio summary.

A project block looks like:

```markdown
### Project N — Name
**Status:** `[~]` In Progress
**Last Step:** Short description of the last completed action
**Next Step:** Short description of what to do next
**Notes:** Any open decisions or blockers
```

---

## Step 3 — Show orientation summary

Before doing any work, display this briefing to the user:

```
## Resuming: [Project Name]

**Status:** [~] In Progress  (or [ ] Not Started)
**Last completed step:** [Last Step value, or "None — starting fresh"]
**Next step:** [Next Step value]
**Open notes/blockers:** [Notes value, or "None"]

---
Checklist progress: X / Y steps done
[ ] Step 1
[x] Step 2
...

Ready to continue. Starting with: [Next Step].
```

Then immediately begin working on the next step without waiting for the user to
say "go" — they invoked this skill to work, not to read a summary.

---

## Step 4 — Execute the next step

Work on the next unchecked checklist item. For each step:

1. Do the actual work — write code, create files, explain concepts, scaffold
   structures — whatever the step requires.
2. When the step is fully complete, use the Edit tool to update the markdown
   file:
   - Change `- [ ] Step text` → `- [x] Step text` for the completed item.
   - Update `**Last Step:**` to describe what was just done.
   - Update `**Next Step:**` to describe the following unchecked item.
   - If this was the last checklist item, update `**Status:**` from `[~]` to `[x]`.

3. Tell the user: "Step done. Updated the tracker. Next: [next step]."

---

## Step 5 — Continue or pause

After each completed step, ask:
> "Continue to the next step, or stop here for today?"

- If the user says **continue / yes / next**: move to the next unchecked item
  and repeat Step 4.
- If the user says **stop / done / pause**: proceed to Step 6.
- If the user does not respond and the session context ends naturally, proceed
  to Step 6.

---

## Step 6 — Update the session log

When the session ends (user says stop, or all steps in the current project are
done), use the Edit tool to append a new row to the Session Log table in the
markdown file:

```markdown
| 2026-03-21 | Project Name | What was done this session | Next session goal |
```

Use today's actual date. Be specific in "What was done" — list the checklist
items completed, not just "worked on project".

---

## Step 7 — Mark project status correctly

After updating the session log:

- If checklist is **partially done**: set `**Status:**` to `` `[~]` In Progress ``
- If checklist is **fully done**: set `**Status:**` to `` `[x]` Done `` and
  update the GitHub Portfolio Summary table row for this project.

---

## Rules

- **Always update the file after every completed step.** Do not batch updates
  to the end of the session — the file is the source of truth. If the session
  ends unexpectedly, the tracker must already reflect real progress.

- **Never skip checklist items.** Work through them in order. If a step has a
  dependency (e.g., "depends on Project 1 being live"), flag it to the user and
  move to the next unblocked item.

- **Never modify the file structure** — only update status markers (`[ ]` →
  `[x]`), the **Last Step**, **Next Step**, **Status** fields, the session log
  table, and the portfolio summary table. Do not rewrite headings, reorder
  sections, or change unrelated content.

- **One project at a time.** If the user asks to switch projects mid-session,
  save progress on the current one first (Step 6), then restart from Step 2 for
  the new project.

- **Be specific in all updates.** "Set up conftest.py with driver fixture" is
  better than "did some pytest work". The file must be useful to a future Claude
  reading it cold.

---

## Example invocations

```
/project-tracker
```
Reads default file, finds active project, resumes.

```
/project-tracker /Users/ahmedhesham/Downloads/01-My Work/OtherProject.md
```
Reads the specified file instead of the default.

```
resume my project
```
Same as `/project-tracker` — reads default file and picks up where left off.
