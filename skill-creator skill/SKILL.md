---
name: skill-creator
description: >
  Use this skill when the user wants to create, generate, scaffold, or improve a
  Claude Code skill. Triggers on phrases like "create a skill", "make a skill for X",
  "turn this into a skill", "update this skill", "improve my skill", or "build a skill
  that does X". Also triggers when the user describes a workflow they want to automate
  and wants it captured as a reusable skill.
version: 2.0.0
---

# Skill Creator

You are the architect of Ahmed's skill library. Your goal is to generate complete,
high-quality, ready-to-use Claude Code skills — with minimal back-and-forth.

Ahmed is a Valeo automotive SW validation engineer transitioning to QA Automation.
His skills cover: ISTQB testing, pytest automation, Selenium, defect reporting,
automotive protocols (UDS, SecOC, SOME/IP, CAN, CANoe), and QA agency tooling.

---

## Core Loop (always follow this sequence)

```
Research → Draft → Test → Benchmark → Review → Improve → Deploy
```

---

## Step 1 — Research First (do not skip)

Before writing a single line of the skill, understand the domain.

1. **Extract intent from conversation** — if the user just finished a workflow with
   you, extract: tools used, steps taken, corrections made, input/output formats.
   The current conversation may already contain the full skill blueprint.

2. **Web search** for any technical subject:
   - `"Best practices for [subject]"`
   - `"Common workflow for [subject]"`
   - `"[subject] checklist / standards / edge cases"`

3. **Synthesize** — use this research to populate the Workflow and Commands
   sections. A skill built on research is always better than one built on guesses.

4. **Ask the user to fill gaps**, then confirm before proceeding:
   - What should this skill enable Claude to do?
   - When should it trigger? (phrases, contexts, keywords)
   - What is the expected output format?
   - Should we set up test cases to verify the skill works?

---

## Step 2 — Define Skill Metadata

Infer from context if not provided:

| Field | Rule |
|-------|------|
| **name** | kebab-case, unique (e.g., `uds-test-writer`, `secoc-validator`) |
| **description** | Trigger sentence — include BOTH what the skill does AND when to use it. Be slightly "pushy": mention edge cases where the skill should trigger even if not explicitly named. |
| **version** | Start at `1.0.0` |

**Good description pattern:**
> "Use this skill when the user asks to X, Y, or Z. Also triggers when the user
> mentions [keywords] or pastes [input type], even if they don't explicitly ask for [skill name]."

---

## Step 3 — Write the SKILL.md

### Anatomy of a skill

```
skill-name/
├── SKILL.md          ← required, YAML frontmatter + markdown instructions
├── scripts/          ← executable code for deterministic/repetitive tasks
├── references/       ← cheat sheets, docs, protocol specs
└── assets/           ← templates, icons, output templates
```

### Loading layers

| Layer | When loaded | Size limit |
|-------|-------------|-----------|
| Frontmatter (name + description) | Always | ~100 words |
| SKILL.md body | When skill triggers | <500 lines ideal |
| Bundled resources | On demand | Unlimited |

Keep SKILL.md under 500 lines. If approaching the limit, split into reference files
with clear pointers to where the model should look next.

### Writing rules

- Use **imperative form**: "Search for...", "Output the result as...", "Never leave..."
- Explain **why** behind every rule — LLMs follow reasoning, not just commands.
  Avoid all-caps MUST/NEVER unless truly critical; prefer "This matters because..."
- Define output formats explicitly with templates, not just descriptions.
- Include concrete examples: Input → Output pairs.
- For multi-domain skills, organize by variant in `references/`:

```
automotive-reporter/
├── SKILL.md
└── references/
    ├── uds.md
    ├── secoc.md
    └── someip.md
```

---

## Step 4 — Write Test Cases

After the first draft, write 2–3 realistic test prompts — the kind of thing
a real user would actually type. Share them: "Here are test cases I'd like to try.
Do these look right, or do you want to add more?" Then wait for confirmation.

Save to `evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's actual task prompt — realistic, specific, with context",
      "expected_output": "Description of what a good output looks like",
      "files": []
    }
  ]
}
```

Good test prompts are **specific and realistic**:
- Bad: `"Write a defect report"`
- Good: `"During SecOC validation on U2A16, the ECU accepted a SOME/IP message
  with corrupted MAC. CANoe 17. SW v2.3.1. Write me a defect report."`

---

## Step 5 — Run Evaluations

This is one continuous sequence — do not stop partway through.

### 5a. Spawn runs (with-skill AND baseline in the same turn)

For each test case, spawn two subagents simultaneously:

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files, or "none">
- Save outputs to: <workspace>/iteration-1/eval-<ID>/with_skill/outputs/
```

**Baseline run** (same prompt, no skill):
```
Execute this task — no skill provided:
- Task: <eval prompt>
- Save outputs to: <workspace>/iteration-1/eval-<ID>/without_skill/outputs/
```

Organize results:
```
<skill-name>-workspace/
└── iteration-1/
    ├── eval-0-<descriptive-name>/
    │   ├── with_skill/outputs/
    │   ├── without_skill/outputs/
    │   ├── eval_metadata.json
    │   └── timing.json
    └── eval-1-<descriptive-name>/
        └── ...
```

### 5b. While runs are in progress — draft assertions

Don't wait idle. Draft quantitative assertions for each test case and explain
them to the user. Good assertions are **objectively verifiable** and have
**descriptive names** readable at a glance in benchmark results.

Subjective outputs (writing style, design) → skip assertions, rely on human review.

Update `eval_metadata.json`:
```json
{
  "eval_id": 0,
  "eval_name": "secoc-corrupted-mac-report",
  "prompt": "The task prompt",
  "assertions": [
    {
      "text": "Output contains a Severity field set to Critical",
      "passed": null,
      "evidence": null
    }
  ]
}
```

### 5c. Capture timing data immediately when each run completes

When a subagent task notification arrives, save immediately to `timing.json`:
```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```
This data is only available in the notification — it is not persisted elsewhere.

### 5d. Grade, aggregate, and show results

1. **Grade** — spawn a grader subagent that evaluates each assertion against
   outputs. Save to `grading.json` in each run directory. Use fields `text`,
   `passed`, `evidence` (these exact names — the viewer depends on them).

2. **Aggregate** — produce a `benchmark.md` summary table:

   | Config | Pass Rate | Avg Time | Avg Tokens |
   |--------|-----------|----------|------------|
   | with_skill | X% | Xs | N |
   | without_skill | X% | Xs | N |
   | delta | +X% | +Xs | +N |

3. **Present results to the user** — show outputs side by side for each test case.
   Ask for feedback inline: "How does this look? Anything you'd change?"

---

## Step 6 — Improve the Skill

This is the heart of the loop.

### How to think about improvements

1. **Generalize from feedback** — you're iterating on 2–3 examples but the skill
   will be used thousands of times. Avoid over-fitting to the test cases. If there's
   a stubborn issue, try a different metaphor or structure rather than adding more
   rigid rules.

2. **Keep the prompt lean** — remove things that aren't pulling their weight.
   Read the transcripts (not just final outputs) — if the model wastes time on
   unproductive steps, cut the part of the skill causing that.

3. **Explain the why** — write rules that explain their reasoning. "Always number
   steps because the reader will reproduce them in isolation" is better than
   "ALWAYS number steps." LLMs follow reasoning, not just commands.

4. **Bundle repeated work** — if all 3 test runs independently wrote the same
   helper script, put it in `scripts/` and reference it from SKILL.md. Save every
   future invocation from reinventing it.

### The iteration loop

```
Improve skill → rerun all test cases → iteration-<N+1>/ → review → repeat
```

Keep iterating until:
- User says they're happy
- All feedback is empty (everything looks good)
- No meaningful progress across two iterations

---

## Step 7 — Optimize the Description (optional but recommended)

The description field is the primary trigger mechanism. After the skill is stable,
offer to optimize it.

1. Generate 20 trigger eval queries — mix of should-trigger (10) and
   should-not-trigger (10). Make them realistic and specific:
   - Bad: `"Write a test"` → too generic
   - Good: `"ok I have this UDS SID 0x27 issue where the ECU returns NRC 0x35
     instead of 0x04 — can you write me a defect report for JIRA?"` → specific

2. The should-not-trigger queries must be **genuine near-misses** — adjacent domain,
   overlapping keywords, but a different tool is actually needed.

3. Share queries with Ahmed for review before running.

4. Apply the best description to SKILL.md frontmatter. Show before/after and
   report the trigger accuracy improvement.

---

## Step 8 — Dual Deployment (MANDATORY — never skip)

After the skill is finalized, **always deploy to both locations**:

### Location 1 — Active (Claude uses this)
```
~/.claude/skills/[skill-name]/
```

### Location 2 — Archived (Ahmed's skill library)
```
/Users/ahmedhesham/Downloads/01-My Work/03-AI_Skills/[skill-name]/
```

Run:
```bash
cp -r ~/.claude/skills/[skill-name] "/Users/ahmedhesham/Downloads/01-My Work/03-AI_Skills/[skill-name]"
```

Then confirm:
```
✅ Skill "[skill-name]" deployed to:
   • ~/.claude/skills/[skill-name]/               ← active (Claude will invoke this)
   • 03-AI_Skills/[skill-name]/                   ← archived in Ahmed's skill library
```

This step is non-negotiable. Every skill must be archived in `03-AI_Skills`
alongside: `istqb-foundation`, `requirements-to-test-cases`, `defect-report-writer`,
`someip-secoc-validator`, `security-sentinel`, `auto-sec-validator`, and others.

---

## Quick Reference — Full Workflow

```
1. Research       → web search + extract intent from conversation
2. Interview      → clarify purpose, trigger phrases, output format
3. Draft SKILL.md → frontmatter + body + supporting files
4. Test cases     → 2–3 realistic prompts → evals/evals.json
5. Run evals      → spawn with-skill + baseline subagents in parallel
6. Review         → grade assertions + show user side-by-side outputs
7. Improve        → generalize feedback → iterate until satisfied
8. Optimize       → description trigger accuracy (optional)
9. Deploy         → ~/.claude/skills/ + 03-AI_Skills/ (mandatory)
```
