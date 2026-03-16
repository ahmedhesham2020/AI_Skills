---
name: skill-creator
description: >
  Use this skill when the user wants to create, generate, scaffold, or improve a
  Claude Code skill. Triggers on phrases like "create a skill", "make a skill for X",
  "turn this into a skill", "update this skill", "improve my skill", "build a skill
  that does X", or "run evals on my skill". Also triggers when the user describes a
  workflow they want to automate and wants it captured as a reusable skill, or when
  they paste a workflow transcript and say "can we make this repeatable".
version: 3.0.0
---

# Skill Creator

You are the architect of Ahmed's skill library. Your goal is to generate complete,
high-quality, ready-to-use skills — with minimal back-and-forth.

Ahmed is a Valeo automotive SW validation engineer transitioning to QA Automation.
His skill library covers: ISTQB testing, pytest automation, Selenium, defect reporting,
CAPL scripting, automotive protocols (UDS, SecOC, SOME/IP, CAN, CANoe), and QA tooling.

Your job is to figure out where the user is in the creation process and jump in to
help them progress. They might say "I want to make a skill for X" — in that case,
start from scratch. Or they might already have a draft — go straight to the eval loop.
Be flexible: if the user says "just vibe with me and skip the evals", do that.

---

## Core Loop

```
Research → Draft → Test → Benchmark → Review → Improve → Deploy
```

---

## Step 1 — Research First

Before writing a single line of the skill, understand the domain.

1. **Extract intent from conversation** — if the user just finished a workflow,
   extract: tools used, steps taken, corrections made, input/output formats. The
   current conversation may already contain the full skill blueprint.

2. **Web search** for any technical subject:
   - `"Best practices for [subject]"`
   - `"Common workflow for [subject]"`
   - `"[subject] checklist / standards / edge cases"`

3. **Synthesize** — use this research to populate the Workflow and Commands sections.
   A skill built on research is always better than one built on guesses.

4. **Clarify gaps with the user**, then confirm before proceeding:
   - What should this skill enable Claude to do?
   - When should it trigger? (phrases, contexts, keywords)
   - What is the expected output format?
   - Should we set up test cases to verify the skill works?

---

## Step 2 — Define Skill Metadata

| Field | Rule |
|-------|------|
| **name** | kebab-case, unique (e.g., `uds-test-writer`, `capl-generator`) |
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
├── SKILL.md          ← required — YAML frontmatter + markdown instructions
├── scripts/          ← executable code for deterministic/repetitive tasks
├── references/       ← cheat sheets, docs, protocol specs
└── assets/           ← templates, icons, output templates
```

### Loading layers

| Layer | When loaded | Size limit |
|-------|-------------|------------|
| Frontmatter (name + description) | Always | ~100 words |
| SKILL.md body | When skill triggers | <500 lines ideal |
| Bundled resources | On demand | Unlimited |

Keep SKILL.md under 500 lines. If approaching the limit, split into reference files
with clear pointers to where the model should look.

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

### Security

Skills must not contain malware, exploit code, or content that could compromise
system security. Don't create skills designed to facilitate unauthorized access,
data exfiltration, or other malicious activities.

---

## Step 4 — Write Test Cases

After the first draft, write 2–3 realistic test prompts — the kind a real user would
actually type. Share them: "Here are test cases I'd like to try. Do these look right,
or do you want to add more?" Then wait for confirmation.

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
- Good: `"During SecOC validation on U2A16, the ECU accepted a SOME/IP message with
  corrupted MAC. CANoe 17. SW v2.3.1. Write me a defect report."`

---

## Step 5 — Run Evaluations

This is one continuous sequence — do not stop partway through.

### 5a. Spawn runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents simultaneously:

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files, or "none">
- Save outputs to: <workspace>/iteration-1/eval-<ID>/with_skill/outputs/
```

**Baseline run** (same prompt, no skill — or old version when improving):
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
```

### 5b. While runs are in progress — draft assertions

Don't wait idle. Draft quantitative assertions for each test case:

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

Subjective outputs (writing style, design) → skip assertions, rely on human review.

### 5c. Capture timing data immediately when each run completes

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This data is only available in the notification — save it immediately to `timing.json`.

### 5d. Grade, aggregate, and launch the viewer

1. **Grade** — spawn a grader subagent (`agents/grader.md`). Save to `grading.json`
   using fields `text`, `passed`, `evidence` (exact names — viewer depends on them).

2. **Aggregate:**
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```

3. **Launch the viewer:**
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   ```
   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **Headless environments:** Use `--static <output_path>` to write a standalone HTML
   file. Feedback downloads as `feedback.json` when the user clicks "Submit All Reviews".

4. **Tell the user:** "I've opened the results in your browser. 'Outputs' tab lets you
   review each test case and leave feedback. 'Benchmark' shows the quantitative comparison.
   Come back when you're done."

---

## Step 6 — Improve the Skill

1. **Generalize from feedback** — you're iterating on 2–3 examples but the skill will
   be used many times. Avoid over-fitting. If there's a stubborn issue, try a different
   metaphor or structure rather than adding more rigid rules.

2. **Keep the prompt lean** — remove things that aren't pulling their weight. Read
   transcripts (not just final outputs) — if the model wastes time on unproductive steps,
   cut the part of the skill causing that.

3. **Explain the why** — write rules that explain their reasoning. "Always number steps
   because the reader will reproduce them in isolation" is better than "ALWAYS number
   steps."

4. **Bundle repeated work** — if all test runs independently wrote the same helper script,
   put it in `scripts/` and reference it from SKILL.md.

### The iteration loop

```
Improve skill → rerun all test cases → iteration-<N+1>/ → review → repeat
```

Keep iterating until:
- User says they're happy
- All feedback is empty
- No meaningful progress across two iterations

---

## Step 7 — Optimize the Description (optional but recommended)

### 7a. Generate trigger eval queries

Create 20 queries — mix of should-trigger (10) and should-not-trigger (10). Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Make them realistic and specific. Near-miss negatives are most valuable — adjacent
domain, overlapping keywords, but a different tool is actually needed.

### 7b. Review with user

1. Read template from `assets/eval_review.html`
2. Replace `__EVAL_DATA_PLACEHOLDER__`, `__SKILL_NAME_PLACEHOLDER__`, `__SKILL_DESCRIPTION_PLACEHOLDER__`
3. Write to `/tmp/eval_review_<skill-name>.html` and open it
4. User edits queries and clicks "Export Eval Set" → downloads `~/Downloads/eval_set.json`

### 7c. Run the optimization loop

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

This runs automatically: 60/40 train/test split, 3 runs per query, extended thinking
to propose improvements, re-evaluation per iteration. Returns `best_description`.

### 7d. Apply the result

Update the skill's SKILL.md frontmatter with `best_description`. Show before/after.

---

## Step 8 — Package (if `present_files` tool is available)

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Present the resulting `.skill` file to the user for download.

---

## Step 9 — Dual Deployment (MANDATORY — never skip)

Every skill must be deployed to **three locations**:

### Location 1 — Active (Claude uses this)
```
~/.claude/skills/[skill-name]/
```

### Location 2 — Claude archive (AI_Skills repo)
```
/Users/ahmedhesham/Downloads/01-My Work/03-AI_Skills/claude/[skill-name]/
```

### Location 3 — Gemini archive (AI_Skills repo)
```
/Users/ahmedhesham/Downloads/01-My Work/03-AI_Skills/gemini/[skill-name]/
```

Run:
```bash
# Copy to active
cp -r <skill-path> ~/.claude/skills/[skill-name]

# Copy to Claude archive (exact copy)
cp -r <skill-path> "/Users/ahmedhesham/Downloads/01-My Work/03-AI_Skills/claude/[skill-name]"

# Copy to Gemini archive (strip version: and replace tool refs)
cp -r <skill-path> "/Users/ahmedhesham/Downloads/01-My Work/03-AI_Skills/gemini/[skill-name]"
sed -i '' '/^version:/d' "/Users/ahmedhesham/Downloads/01-My Work/03-AI_Skills/gemini/[skill-name]/SKILL.md"
```

Apply Gemini transformations per `03-AI_Skills/CLAUDE.md`:
- Remove `version:` from frontmatter
- Replace `$ARGUMENTS` → `the user's request`
- Replace `Use the Write tool to` → `Write a file named`
- Replace `Use the Bash tool to run` → `Run the command`
- Replace `Use the Read tool to` → `Read`

### Update the repo README

Add the new skill entry to `03-AI_Skills/README.md` following the existing numbered list format:

```
### [N]. [Skill Display Name]
- **Goal:** One sentence — what does this skill produce?
- **Use when:** Trigger phrases and scenarios.
- **Outputs:** File types and deliverables generated.
```

Then confirm:
```
✅ Skill "[skill-name]" deployed to:
   • ~/.claude/skills/[skill-name]/                                    ← active
   • 03-AI_Skills/claude/[skill-name]/                                 ← Claude archive
   • 03-AI_Skills/gemini/[skill-name]/                                 ← Gemini archive
   • 03-AI_Skills/README.md                                            ← updated
```

---

## Communicating with the user

Pay attention to context cues to understand technical familiarity:
- "evaluation" and "benchmark" are borderline, but OK for most users
- "JSON" and "assertion" — explain if user doesn't seem technical
- Brief term definitions are always welcome if in doubt

---

## Claude.ai-specific instructions

**Running test cases:** No subagents — run test prompts yourself, one at a time.
Skip baseline runs.

**Reviewing results:** No browser — present results inline in the conversation.
Show prompt + output per test case, ask for feedback inline.

**Benchmarking:** Skip quantitative benchmarking. Focus on qualitative feedback.

**Description optimization:** Requires `claude` CLI — skip on Claude.ai.

**Packaging:** `package_skill.py` works anywhere with Python.

---

## Cowork-specific instructions

- Subagents available — main workflow runs normally.
- No browser — use `--static <output_path>` for the eval viewer.
- **ALWAYS generate the eval viewer before evaluating inputs yourself.** Get outputs
  in front of the human ASAP using `generate_review.py`.
- Feedback downloads as `feedback.json` when user clicks "Submit All Reviews".
- Description optimization (`run_loop.py`) works fine in Cowork.

---

## Quick Reference

```
1. Research       → web search + extract intent from conversation
2. Interview      → clarify purpose, trigger phrases, output format
3. Draft SKILL.md → frontmatter + body + supporting files
4. Test cases     → 2–3 realistic prompts → evals/evals.json
5. Run evals      → spawn with-skill + baseline subagents in parallel
6. Review         → grade assertions + show user side-by-side outputs
7. Improve        → generalize feedback → iterate until satisfied
8. Optimize       → description trigger accuracy (optional)
9. Package        → .skill file (if present_files available)
10. Deploy        → ~/.claude/skills/ + 03-AI_Skills/claude/ + 03-AI_Skills/gemini/ + update README.md
```

## Reference files

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another
- `references/schemas.md` — JSON structures for evals.json, grading.json, benchmark.json
