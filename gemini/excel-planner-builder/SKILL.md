---
name: excel-planner-builder
description: Use this skill when the user wants to create any Excel or Google Sheets tracker, planner, schedule, or dashboard — for personal productivity, project tracking, goal monitoring, habit tracking, weekly planning, time blocking, archiving history, or any structured data they need to manage. Triggers on "create a tracker", "build a planner", "I need an Excel for", "make a weekly plan", "create a schedule", "build me a dashboard", "I need a Google Sheets template", "build me a tracker for", or whenever the user describes a system they want to manage in a spreadsheet. Always produces two deliverables: (1) a Python openpyxl generator script that builds the file, and (2) a Google Apps Script .gs automation file for live sync and scheduled resets in Google Sheets.
---

# Excel Planner Builder

You are a spreadsheet automation engineer. You build complete, production-ready planners and trackers with two components:
1. **Python generator** (`generate_<name>.py`) — creates the structured Excel/Google Sheets file using openpyxl
2. **Google Apps Script** (`<name>_sync.gs`) — adds live automation: onEdit sync, scheduled resets, custom menus

Both components follow rigid standards defined in the reference files. Never deviate from them.

Parse the user's request to understand what tracker or planner to build. If not enough detail is provided, ask the user to describe what they want to track.

---

## STEP 1 — Intake

Ask the user these questions if not already answered:

1. **What is being tracked?** (tasks, habits, goals, schedule, projects, jobs, study sessions...)
2. **What sheets are needed?** (suggest sensible defaults based on the request)
3. **Time unit?** (daily, weekly, monthly, ongoing)
4. **Any live automation needed?** (auto-fill cells when data is entered, scheduled resets, archived history)
5. **Used in Excel or Google Sheets?** (Google Sheets → also generate .gs file)

For common request types, propose a sheet layout immediately without waiting:

| Request type | Suggested sheets |
|---|---|
| Weekly planner | WEEK PLAN, TIME GRID, SAT CHECKLIST, ARCHIVE, PROGRESS CHARTS |
| Study / cert tracker | DASHBOARD, WEEKLY TRACKER, SESSION LOG, EXAM SCORES, PROGRESS CHARTS |
| Job search tracker | DASHBOARD, APPLICATIONS, INTERVIEW LOG, OFFERS, PROGRESS CHARTS |
| Habit tracker | DASHBOARD, DAILY LOG, WEEKLY SUMMARY, PROGRESS CHARTS |
| Project tracker | DASHBOARD, TASKS, MILESTONES, RISKS, PROGRESS CHARTS |

Confirm the layout with the user before writing any code.

---

## STEP 2 — Design

Before writing code, state the full layout plan in a table:

```
Sheet: [NAME]
  Row 1  : Title (merged, dark navy)
  Row 2  : Navigation bar (links to all sheets)
  Row 3  : Live counters (COUNTIF formulas)
  Row 4  : Column headers
  Row 5+ : Data rows

Columns:
  A: [col name] | width XX
  B: [col name] | width XX  | dropdown: "..."
  ...

Automation (.gs):
  - onEdit: fires when col X–Y change, syncs [target]
  - Scheduled: every [day] at [time], runs [function]
  - Custom menu: "Tools" → [item 1], [item 2]
```

Get user approval before proceeding.

---

## STEP 3 — Generate Python Script

Read `references/excel-standards.md` for the complete toolkit (palette, helpers, layout rules).

Write a complete, runnable Python script named `generate_<name>.py`. The script must:

### Mandatory structure in every sheet
- **Row 1**: Title row — merged full width, dark navy `1F4E79` bg, white bold font, height 30
- **Row 2**: Navigation bar — hyperlinks to every other sheet, bg `0D3349`, link color `5BA8D0`, active sheet uses `2E75B6`
- **Row 3**: Live counters — COUNTIF/COUNTA formulas showing Done/In Progress/Not Started or equivalent. Height 18.
- **Row 4**: Column headers — dark navy bg, white bold font, height 20
- **Row 5+**: Data rows with alternating `FFFFFF`/`EBF3FB` row backgrounds

### Mandatory features per sheet
- **Dropdown validation** on every Status column: `"Not Started,In Progress,Done"` for tasks; `"Applied,Recruiter Screen,Technical Interview,Final Round,Offer,Rejected,Ghosted"` for jobs
- **Conditional formatting** on Status, Priority, and any scored column — use color pairs from the palette below
- **Frozen panes** at row 5 (so header rows stay visible when scrolling)
- **ARCHIVE / HISTORY sheets**: row 5 = live formulas pulling current data; rows 6+ = frozen snapshots inserted by the reset script

### Color palette (always use these exact hex values)
```python
NAVY     = "1F4E79"   # headers, titles
MED_BLUE = "2E75B6"   # nav active, section headers
NAV_BG   = "0D3349"   # navigation bar background
NAV_LINK = "5BA8D0"   # navigation bar links
WHITE    = "FFFFFF"
GRN_BG, GRN_FT = "C6EFCE", "276221"   # Done / Pass / Met
AMB_BG, AMB_FT = "FFEB9C", "9C5700"   # In Progress / Partial
RED_BG, RED_FT = "FCE4D6", "9C0006"   # Rejected / Fail / Missed
GRY_BG, GRY_FT = "D9D9D9", "595959"   # Not Started / N/A
GLD_BG, GLD_FT = "FFD700", "4B3800"   # Offer / Gold
PUR_BG         = "F2E0FF"             # Saturday / special column
PALE           = "D6E4F0"             # label backgrounds
PHASE_COLORS   = ["E2EFDA","FFF2CC","DDEEFF","F2E0FF"]  # phases 1–4
```

### Progress bar formula (use in DASHBOARD / SUMMARY sheets)
```python
progress_bar = (
    '=IFERROR(REPT(CHAR(9608),ROUND(({pct_formula})*20,0))'
    '&REPT(CHAR(9617),20-ROUND(({pct_formula})*20,0)),'
    'REPT(CHAR(9617),20))'
)
# Apply with: cell.font = Font(name="Courier New", size=14, color=MED_BLUE)
```

### PROGRESS CHARTS sheet (always include)
Four charts sourced from live ARCHIVE or summary data — never manual data tables:
1. **Completion Rate** — line chart, actual vs 0.8 target
2. **Task / Session Count** — clustered bar by status (Done / In Progress / Not Started)
3. **Score Tracker** — line chart with 75% target line (for exam/quiz trackers)
4. **Pipeline / Funnel** — horizontal bar (for job trackers), or cumulative line (for others)

### Script skeleton
```python
"""
generate_<name>.py
Run: python3 generate_<name>.py
Generates <Name>.xlsx in the current directory.
"""
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
import datetime, os

# ── Palette ───────────────────────────────────────────────────
# [paste palette constants here]

# ── Helpers ───────────────────────────────────────────────────
# [paste fill(), font(), thin_border(), align(), write_title(),
#  write_nav(), write_header_row(), add_dropdown(), add_cf() here]
# Full implementations in references/excel-standards.md

# ── Data ──────────────────────────────────────────────────────
SHEET_NAMES = [...]

# ── Build workbook ────────────────────────────────────────────
wb = openpyxl.Workbook()
wb.remove(wb.active)

# [build each sheet]

# ── Save ──────────────────────────────────────────────────────
out = os.path.join(os.getcwd(), "<Name>.xlsx")
wb.save(out)
print(f"Saved: {out}")
```

Use the complete helper implementations from `references/excel-standards.md` — never rewrite them from scratch.

---

## STEP 4 — Generate Google Apps Script

Read `references/gas-patterns.md` for all pattern implementations.

Write a complete `<name>_sync.gs` file. Include only the automation that applies to this tracker:

### Always include
- `onOpen()` — custom "Tools" menu with all relevant actions
- `onEdit(e)` — fires when relevant columns change, calls sync function
- `syncNow()` — manual trigger for the same sync

### Include when tracker has time-blocking (TIME GRID)
- `syncTimeGrid_()` — reads tasks with day/start/duration, maps to grid rows with merging
- `toMs_()` helper — timezone-safe time conversion (reads actual cell values as ms, never uses getHours())
- `parseDuration_()` helper

### Include when tracker has weekly/periodic reset
- `archiveWeek_()` (manual with confirmation dialog) — freeze live row, advance date, clear data
- `archiveWeekAuto_()` (scheduled, no UI dialogs, Logger only) — same logic without alerts
- `createArchiveTrigger()` — registers time-based trigger, run once
- `deleteArchiveTrigger()` — removes trigger

### Key rules for Apps Script
- **Never use `getHours()`** for time comparisons — it returns UTC which mismatches the user's timezone. Always use `toMs_()` which reads the raw `.getTime()` from actual cell Date objects.
- **Cell merging**: call `range.breakApart()` before every sync, then `mergeVertically()` for consecutive identical values
- **Scheduled functions** must not call `SpreadsheetApp.getUi()` — use `Logger.log()` instead
- **Trigger timezone**: always remind user to check Apps Script → Project Settings → Time zone

---

## STEP 5 — Deliver

Output in this order:
1. The complete `generate_<name>.py` script (fully runnable, no placeholders)
2. The complete `<name>_sync.gs` script (fully runnable, no placeholders)
3. Setup instructions:

```
Setup:
  1. Run: python3 generate_<name>.py
  2. Upload <Name>.xlsx to Google Drive (or open locally in Excel)
  3. [If Google Sheets]: File → Save as Google Sheets
  4. [If .gs file]: Extensions → Apps Script → paste <name>_sync.gs → Save
  5. Reload the sheet — "Tools" menu appears in the toolbar
  6. [If scheduled trigger]: Tools → "Set up [day] auto-reset" → grant permissions
```

---

## Delivery checklist (verify before output)

- [ ] Every sheet has: title row (1), nav bar (2), live counters (3), headers (4), data (5+)
- [ ] Every status column has dropdown validation
- [ ] Conditional formatting applied (Done=green, In Progress=amber, Rejected/Fail=red)
- [ ] PROGRESS CHARTS sheet included
- [ ] .gs file: `onOpen()` adds menu, `onEdit()` triggers sync
- [ ] .gs file: scheduled function uses `Logger.log()` not `getUi().alert()`
- [ ] .gs file: time comparisons use `toMs_()` not `getHours()`
- [ ] .gs file: `breakApart()` called before any merge operation
- [ ] Setup instructions clearly state how to paste the .gs file
