# Prompt Architect — Skill Reference

Transforms a rough user request into a complete, structured prompt with six labeled sections: Role, Task, Context Block, Goal/Stakes, Completion Criteria, and Output Format.

---

## Trigger

```
/prompt-architect [rough description of what you want]
```

Also activates on natural-language phrases: "give me a prompt", "create a prompt for", "build a prompt", "generate a Claude prompt", "turn this into a prompt", "make a structured prompt", "write a prompt for"

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Rough description | Yes | Plain English: what you want to accomplish |
| Domain / industry | Helpful | Detected from keywords; asked if absent |
| Audience | Helpful | Who reads or uses the output |
| Constraints | Helpful | Budget, team size, timeline, skill level |

If fewer than 2 context signals are present, the skill asks 3 clarifying questions before generating.

---

## Output — The Six Sections

| Section | Label | What it does |
|---------|-------|-------------|
| Role | `[Role]` | Expert identity + domain + one explicit priority bias |
| Task | `[Task]` | Specific deliverable + upstream goal + terminal artifact |
| Context Block | `[Context Block]` | "Here's what I know:" bullet facts (4–7 items) |
| Goal/Stakes | `[Goal/Stakes]` | Why this matters + quality-enforcement mechanism |
| Completion Criteria | `[Completion Criteria]` | "Only stop when:" binary, measurable checklist (3–6 items) |
| Output Format | `[Output Format]` | Presentation structure + field definitions per repeating unit |

---

## Example Usage

**Rich input (generates immediately):**
```
/prompt-architect
Build a 90-day launch plan for a new AI productivity tool for founders.
2-person team, lean budget, 15-20 beta users. Key risks: adoption, retention, positioning.
```

**Thin input (asks clarifying questions first):**
```
/prompt-architect I need a prompt to review my test suite
```
→ Skill detects thin input and asks 3 clarifying questions before generating.

---

## File Structure

```
claude/prompt-architect/
├── SKILL.md     ← Main skill definition
└── README.md    ← This file
```
