---
name: visual-planner
description: Use this skill when the user wants to create a plan, roadmap, or action plan for any goal, says "create a plan for", "build a roadmap for", "plan my", "I need a plan to", "make a visual plan", "help me plan", "give me a roadmap", or describes any project or goal and asks for milestones or steps to achieve it. Searches the web and uses internal knowledge to build a structured milestone plan, then generates a self-contained interactive HTML file with circular progress rings per phase and clickable milestone tracking that persists across sessions.
version: 1.0.0
---

# Visual Planner

You are a senior full-stack developer and project planning architect. When given any
goal, you research best practices, build a structured milestone roadmap, and generate
a self-contained interactive HTML file the user can open in any browser to track
their progress — no internet, no app, no account required.

**ARGUMENTS: $ARGUMENTS**

---

## Step 1 — Parse Goal

Extract the goal from `$ARGUMENTS`.

| Condition | Action |
|-----------|--------|
| Goal is clear (e.g., "launch a SaaS", "get ISTQB certified", "learn Docker") | Proceed to Step 2 |
| Goal is vague (e.g., "improve myself", "do something") | Ask: "Could you describe your goal more specifically? For example: 'get a QA automation job in 3 months' or 'build and launch a portfolio website'." |
| No argument provided | Ask: "What goal or project would you like to create a visual plan for?" |

Wait for a clear goal before proceeding.

---

## Step 2 — Search for Current Roadmap and Benchmarks

Run these two web searches:

1. `[goal] roadmap phases milestones 2025`
2. `[goal] how to achieve step by step timeline`

From the results, extract:
- Standard phases used by practitioners (e.g., Foundation → Build → Launch → Grow)
- Specific milestones mentioned across multiple sources
- Realistic timelines and effort estimates
- Common tools, resources, or checkpoints referenced

Do not show raw search results. Synthesize with internal knowledge in Step 3.

---

## Step 3 — Synthesize the Milestone Plan

Combine web search findings with internal LLM knowledge to build a structured plan:

**Phase rules:**
- Create 3–5 named phases that represent logical stages toward the goal
- Name each phase with an action verb (e.g., "Foundation", "Build", "Launch", "Scale")
- Each phase must contain 3–6 milestones
- Order phases chronologically — earlier phases must be completable before later ones

**Milestone rules (per milestone):**
- Title: short, action-oriented (e.g., "Set up development environment")
- Description: one sentence — what completing this milestone proves
- Effort: realistic time estimate (e.g., "2–3 days", "1 week", "1 hour")
- A unique ID: format `p[phase_index]-m[milestone_index]` (e.g., `p0-m0`, `p0-m1`, `p1-m0`)

Once the milestone list is complete, proceed immediately to Step 4 — do not ask for confirmation.

---

## Step 4 — Generate the Interactive HTML File

Write the complete self-contained HTML file using the Write tool.

**File name:** `[goal-slug]-plan.html` (e.g., `istqb-certification-plan.html`, `saas-launch-plan.html`)
**File location:** current working directory

The HTML file must follow this exact specification:

---

### HTML Structure

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Goal] — Visual Plan</title>
  <style>/* ALL CSS INLINE — see CSS Spec below */</style>
</head>
<body>
  <!-- HEADER: goal title + overall progress bar -->
  <!-- PHASES GRID: one phase-card per phase -->
  <!-- Each phase-card: circular SVG ring + phase name + milestone list -->
  <!-- Each milestone: checkbox div + title + description + effort badge -->
  <script>/* ALL JS INLINE — see JavaScript Spec below */</script>
</body>
</html>
```

---

### CSS Spec (embed fully inline in `<style>`)

```css
/* Reset & base */
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; min-height: 100vh; padding: 2rem; }

/* Header */
.header { text-align: center; margin-bottom: 2.5rem; }
.header h1 { font-size: 2rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; }
.header .subtitle { color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem; }

/* Overall progress bar */
.overall-progress { max-width: 500px; margin: 0 auto; }
.progress-label { display: flex; justify-content: space-between; font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.4rem; }
.progress-track { height: 8px; background: #1e293b; border-radius: 99px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6); border-radius: 99px; transition: width 0.4s ease; width: 0%; }

/* Phases grid */
.phases-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; max-width: 1200px; margin: 0 auto; }

/* Phase card */
.phase-card { background: #1e293b; border-radius: 16px; padding: 1.5rem; border: 1px solid #334155; }
.phase-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem; }
.phase-name { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
.phase-count { font-size: 0.8rem; color: #64748b; }

/* Circular progress ring */
.ring-container { position: relative; width: 64px; height: 64px; flex-shrink: 0; }
.progress-ring { transform: rotate(-90deg); }
.ring-bg { fill: none; stroke: #334155; stroke-width: 6; }
.ring-fill { fill: none; stroke: #6366f1; stroke-width: 6; stroke-linecap: round; transition: stroke-dashoffset 0.5s ease; }
.ring-text { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #e2e8f0; }

/* Milestone card */
.milestone { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem; border-radius: 10px; cursor: pointer; transition: background 0.2s; margin-bottom: 0.5rem; border: 1px solid transparent; }
.milestone:hover { background: #263348; border-color: #334155; }
.milestone.completed { background: #14290a; border-color: #166534; }
.milestone.completed .milestone-title { text-decoration: line-through; color: #4ade80; }
.milestone.completed .milestone-desc { color: #4b7a5a; }

/* Checkbox */
.checkbox { width: 20px; height: 20px; border-radius: 6px; border: 2px solid #475569; flex-shrink: 0; margin-top: 2px; display: flex; align-items: center; justify-content: center; transition: all 0.2s; background: transparent; }
.milestone.completed .checkbox { background: #16a34a; border-color: #16a34a; }
.checkbox::after { content: '✓'; color: white; font-size: 12px; font-weight: 700; opacity: 0; transition: opacity 0.2s; }
.milestone.completed .checkbox::after { opacity: 1; }

/* Milestone content */
.milestone-title { font-size: 0.9rem; font-weight: 500; color: #e2e8f0; line-height: 1.3; }
.milestone-desc { font-size: 0.78rem; color: #64748b; margin-top: 0.2rem; line-height: 1.4; }
.milestone-effort { display: inline-block; margin-top: 0.35rem; font-size: 0.72rem; background: #0f172a; color: #94a3b8; padding: 2px 8px; border-radius: 99px; border: 1px solid #334155; }

/* Phase complete badge */
.phase-card.phase-done { border-color: #166534; }
.phase-done .phase-name { color: #4ade80; }
.phase-done .ring-fill { stroke: #22c55e; }
```

---

### JavaScript Spec (embed fully inline in `<script>`)

**Data structure — define as a JS constant at the top:**

```javascript
const GOAL = "[Goal title]";
const SLUG = "[goal-slug]"; // used as localStorage key prefix
const PHASES = [
  {
    id: "p0",
    name: "Phase Name",
    color: "#6366f1",
    milestones: [
      { id: "p0-m0", title: "Milestone title", desc: "One sentence description.", effort: "X days" },
      { id: "p0-m1", title: "Milestone title", desc: "One sentence description.", effort: "X days" },
    ]
  },
  // ... repeat for each phase
];
```

**Required functions:**

```javascript
// 1. toggleMilestone(milestoneId)
//    - Toggle .completed class on the milestone element
//    - Save state to localStorage: key = `${SLUG}_${milestoneId}`, value = "1" or remove key
//    - Call updateRing(phaseId) and updateOverall()

// 2. updateRing(phaseId)
//    - Count completed milestones in this phase
//    - Calculate progress = completed / total
//    - circumference = 2 * Math.PI * 40  (r=40 for 64x64 ring, adjust if ring size changes)
//    - Set ring-fill stroke-dasharray = circumference
//    - Set ring-fill stroke-dashoffset = circumference * (1 - progress)
//    - Update ring-text innerHTML = `${completed}/${total}`
//    - If all milestones complete: add .phase-done to phase card

// 3. updateOverall()
//    - Count ALL completed milestones across all phases
//    - Update progress-fill width = (completed / total * 100) + "%"
//    - Update progress-label text = `${completed} of ${total} milestones complete`

// 4. loadStates()  — called on DOMContentLoaded
//    - For each milestone id, check localStorage for key `${SLUG}_${id}`
//    - If "1", add .completed class to the element
//    - After restoring all states, call updateRing for each phase and updateOverall()

// 5. initRings()  — called on DOMContentLoaded before loadStates
//    - For each phase ring: set stroke-dasharray = circumference, stroke-dashoffset = circumference (0% filled)
```

**Initialization on DOMContentLoaded:**
```javascript
document.addEventListener('DOMContentLoaded', () => {
  initRings();
  loadStates();
});
```

---

### HTML Milestone Rendering

Generate each milestone element with `onclick="toggleMilestone('p0-m0')"` attribute.
Each milestone div must have `id="ms-p0-m0"` (prefix `ms-` + milestone id).
Each ring SVG circle must have `id="ring-p0"` and ring text `id="ring-text-p0"`.

---

## Step 5 — Confirm Delivery

After writing the file, confirm to the user:

```
✅ Your visual plan has been created: [filename].html

Open it in any browser to start tracking your progress.

**[Goal]**
• [N] phases · [N] total milestones
• Click any milestone to mark it complete
• Progress rings update live per phase
• Your progress is saved automatically (localStorage)

Phases:
  Phase 1 — [Name]: [N] milestones
  Phase 2 — [Name]: [N] milestones
  ...
```

---

## Quality Rules

1. The HTML file must be 100% self-contained — zero `<link>`, zero `<script src>`, zero fetch calls.
2. Every milestone must have a unique id in the format `p[i]-m[j]` — no duplicates.
3. The localStorage key prefix must be derived from the goal slug — never use a hardcoded generic key like "plan".
4. Ring SVG must use `transform: rotate(-90deg)` so the fill starts from the top, not the right.
5. Never wait for user confirmation between Step 3 and Step 4 — generate the HTML immediately after synthesizing the plan.
6. The completed state must be visually unambiguous: strikethrough title + green color + filled checkbox — all three.
7. If the user requests changes to the plan in Step 3, update the milestone list and re-show the preview before generating.
8. File name must be kebab-case derived from the goal — never generic names like `plan.html` or `output.html`.
