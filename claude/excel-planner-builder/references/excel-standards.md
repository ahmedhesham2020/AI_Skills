# Excel Generation Standards — openpyxl Toolkit

Complete, copy-paste-ready helper implementations for every Excel generator script.

---

## Full Palette

```python
NAVY     = "1F4E79"
MED_BLUE = "2E75B6"
NAV_BG   = "0D3349"
NAV_LINK = "5BA8D0"
WHITE    = "FFFFFF"
BLACK    = "000000"

GRN_BG, GRN_FT = "C6EFCE", "276221"
AMB_BG, AMB_FT = "FFEB9C", "9C5700"
RED_BG, RED_FT = "FCE4D6", "9C0006"
GRY_BG, GRY_FT = "D9D9D9", "595959"
GLD_BG, GLD_FT = "FFD700", "4B3800"
BLU_BG, BLU_FT = "DDEBF7", "1F4E79"
PUR_BG         = "F2E0FF"
PUR_LINK_BG    = "EDD9FF"
PALE           = "D6E4F0"
PALE_ALT       = "EBF3FB"

PHASE_COLORS = ["E2EFDA", "FFF2CC", "DDEEFF", "F2E0FF"]
```

---

## Core Helpers

```python
def fill(hex_color):
    return PatternFill(fill_type="solid", fgColor=hex_color)

def font(color=BLACK, bold=False, size=11, name="Calibri", italic=False):
    return Font(name=name, size=size, bold=bold, color=color, italic=italic)

def thin_border():
    s = Side(style="thin", color="BFBFBF")
    return Border(left=s, right=s, top=s, bottom=s)

def align(h="left", v="center", wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def center():
    return Alignment(horizontal="center", vertical="center", wrap_text=True)

def left():
    return Alignment(horizontal="left", vertical="center", wrap_text=True)
```

---

## Layout Builders

```python
def write_title(ws, title, num_cols, color=NAVY):
    """Row 1: merged title bar."""
    ws.row_dimensions[1].height = 30
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_cols)
    c = ws.cell(1, 1, title)
    c.fill = fill(color)
    c.font = font(WHITE, bold=True, size=14)
    c.alignment = center()


def write_nav(ws, all_sheets, current_sheet, num_cols):
    """Row 2: navigation bar with hyperlinks to every sheet."""
    ws.row_dimensions[2].height = 18
    # Fill entire row with nav background
    for col in range(1, num_cols + 1):
        ws.cell(2, col).fill = fill(NAV_BG)
    # Write links (one per sheet, left-to-right)
    for i, name in enumerate(all_sheets, 1):
        c = ws.cell(2, i)
        c.value = name
        c.hyperlink = f"#'{name}'!A1"
        is_active = (name == current_sheet)
        c.font = Font(
            color=(MED_BLUE if is_active else NAV_LINK),
            bold=is_active,
            size=10,
            underline="single",
            name="Calibri",
        )
        c.fill = fill(NAV_BG)
        c.alignment = center()


def write_counter_row(ws, label_value_pairs, num_cols):
    """Row 3: alternating label/value counter cells with COUNTIF formulas.
    label_value_pairs = [("Label", "=COUNTIF(...)"), ...]
    """
    ws.row_dimensions[3].height = 18
    for col in range(1, num_cols + 1):
        ws.cell(3, col).fill = fill(PALE)
    for i, (label, formula) in enumerate(label_value_pairs, 1):
        lc = ws.cell(3, i * 2 - 1, label)
        lc.font = font(NAVY, bold=True, size=9)
        lc.fill = fill(PALE)
        lc.alignment = center()
        vc = ws.cell(3, i * 2, formula)
        vc.font = font(RED_FT, bold=True, size=11)
        vc.fill = fill(PALE_ALT)
        vc.alignment = center()


def write_header_row(ws, row_num, headers, col_widths):
    """Write a styled header row and set column widths."""
    ws.row_dimensions[row_num].height = 20
    for i, (h, w) in enumerate(zip(headers, col_widths), 1):
        ws.column_dimensions[get_column_letter(i)].width = w
        c = ws.cell(row_num, i, h)
        c.fill = fill(NAVY)
        c.font = font(WHITE, bold=True)
        c.alignment = center()
        c.border = thin_border()
```

---

## Data Row Helper

```python
def write_data_row(ws, row_num, values, height=22):
    """Write a data row with alternating background and borders."""
    ws.row_dimensions[row_num].height = height
    bg = WHITE if row_num % 2 != 0 else PALE_ALT
    for col_i, val in enumerate(values, 1):
        c = ws.cell(row_num, col_i, val)
        c.fill = fill(bg)
        c.border = thin_border()
        c.alignment = left()
```

---

## Dropdown Validation

```python
def add_dropdown(ws, col_letter, min_row, max_row, options_str):
    """Add dropdown validation to a column range.
    options_str examples:
      '"Not Started,In Progress,Done"'
      '"Applied,Recruiter Screen,Technical Interview,Final Round,Offer,Rejected,Ghosted"'
      '"Pass,Fail,Blocked,Not Run,Skipped"'
    """
    dv = DataValidation(type="list", formula1=options_str, allow_blank=True)
    dv.sqref = f"{col_letter}{min_row}:{col_letter}{max_row}"
    ws.add_data_validation(dv)
```

---

## Conditional Formatting

```python
def add_cf(ws, col_letter, min_row, max_row, rules):
    """Apply cell-value conditional formatting.
    rules = [("value", "bg_hex", "font_hex"), ...]
    Uses FormulaRule for compatibility with openpyxl 3.1+.
    """
    rng = f"{col_letter}{min_row}:{col_letter}{max_row}"
    for val, bg, ft in rules:
        ws.conditional_formatting.add(rng, FormulaRule(
            formula=[f'{col_letter}{min_row}="{val}"'],
            stopIfTrue=False,
            fill=fill(bg),
            font=Font(color=ft),
        ))

# Pre-built sets — call these directly
def add_cf_task_status(ws, col_letter, min_row, max_row):
    add_cf(ws, col_letter, min_row, max_row, [
        ("Done",        GRN_BG, GRN_FT),
        ("In Progress", AMB_BG, AMB_FT),
        ("Not Started", GRY_BG, GRY_FT),
    ])

def add_cf_test_status(ws, col_letter, min_row, max_row):
    add_cf(ws, col_letter, min_row, max_row, [
        ("Pass",    GRN_BG, GRN_FT),
        ("Fail",    RED_BG, RED_FT),
        ("Blocked", AMB_BG, AMB_FT),
        ("Not Run", GRY_BG, GRY_FT),
        ("Skipped", BLU_BG, BLU_FT),
    ])

def add_cf_job_status(ws, col_letter, min_row, max_row):
    add_cf(ws, col_letter, min_row, max_row, [
        ("Offer",              GLD_BG, GLD_FT),
        ("Final Round",        GRN_BG, GRN_FT),
        ("Technical Interview",AMB_BG, AMB_FT),
        ("Recruiter Screen",   BLU_BG, BLU_FT),
        ("Applied",            GRY_BG, GRY_FT),
        ("Rejected",           RED_BG, RED_FT),
        ("Ghosted",            RED_BG, RED_FT),
    ])

def add_cf_priority(ws, col_letter, min_row, max_row):
    add_cf(ws, col_letter, min_row, max_row, [
        ("High",   RED_BG, RED_FT),
        ("Medium", AMB_BG, AMB_FT),
        ("Low",    GRY_BG, GRY_FT),
    ])

def add_cf_goals_met(ws, col_letter, min_row, max_row):
    add_cf(ws, col_letter, min_row, max_row, [
        ("Met",     GRN_BG, GRN_FT),
        ("Partial", AMB_BG, AMB_FT),
        ("Missed",  RED_BG, RED_FT),
    ])
```

---

## Progress Bar

```python
# In the cell value:
def progress_bar_formula(done_formula, total_formula):
    """Returns an Excel formula string that renders a Unicode block progress bar.
    done_formula  — e.g. "COUNTIF(H5:H35,\"Done\")"
    total_formula — e.g. "COUNTA(B5:B35)"
    """
    pct = f"IFERROR(({done_formula})/({total_formula}),0)"
    return (
        f'=IFERROR('
        f'REPT(CHAR(9608),ROUND(({pct})*20,0))'
        f'&REPT(CHAR(9617),20-ROUND(({pct})*20,0)),'
        f'REPT(CHAR(9617),20))'
    )

# Apply like this:
# cell.value = progress_bar_formula("COUNTIF(H5:H35,\"Done\")", "COUNTA(B5:B35)")
# cell.font  = Font(name="Courier New", size=14, color=MED_BLUE)
# cell.alignment = left()
```

---

## ARCHIVE Live Row (current-week formulas)

Use these formula patterns in the live row (always row 5) of any ARCHIVE or HISTORY sheet.

```python
# Column A: auto-incrementing week/entry number
arc.cell(5, 1).value = '=IFERROR(A6+1,1)'

# Column B: date range string from a start-date input cell (e.g. K1 in WEEK PLAN)
arc.cell(5, 2).value = (
    "=IFERROR(TEXT('WEEK PLAN'!K1,\"DD MMM\")"
    "&\" – \""
    "&TEXT('WEEK PLAN'!K1+6,\"DD MMM YYYY\"),\"—\")"
)

# Column C: start date formatted
arc.cell(5, 3).value = "=IFERROR(TEXT('WEEK PLAN'!K1,\"DD MMM YYYY\"),\"—\")"

# Column D: goals met (from SAT CHECKLIST goal status cells)
arc.cell(5, 4).value = (
    "=IF(COUNTIF('SAT CHECKLIST'!E12:E14,\"Done\")=3,\"Met\","
    "IF(COUNTIF('SAT CHECKLIST'!E12:E14,\"Done\")>=1,\"Partial\",\"Missed\"))"
)

# Column E: tasks done
arc.cell(5, 5).value = "=COUNTIF('WEEK PLAN'!H5:H35,\"Done\")"

# Column F: tasks total
arc.cell(5, 6).value = "=COUNTA('WEEK PLAN'!B5:B35)"

# Column G: completion %
arc.cell(5, 7).value = '=IFERROR(E5/F5,"—")'
arc.cell(5, 7).number_format = "0%"

# Column K: not done count (for charts)
arc.cell(5, 11).value = '=IFERROR(F5-E5,"")'
```

---

## TIME GRID Column A (slot times)

Populate column A of TIME GRID with `datetime.time` objects — Google Sheets and Excel both store these as time values the .gs script can read.

```python
import datetime
from openpyxl.styles import numbers

TG_HOUR_START = 6    # 06:00
TG_ROW_START  = 5    # row 5 = first slot
TG_ROW_END    = 22   # row 22 = 23:00

for h in range(TG_HOUR_START, TG_HOUR_START + (TG_ROW_END - TG_ROW_START + 1)):
    row = h - TG_HOUR_START + TG_ROW_START
    c = tg_ws.cell(row=row, column=1, value=datetime.time(h, 0))
    c.number_format = "HH:MM"
    c.font = font(NAVY, bold=True, size=10)
    c.alignment = center()
```

---

## Layout Constants Pattern

Always define these at the top of every generator:

```python
# Row layout (applies to every sheet)
ROW_TITLE   = 1
ROW_NAV     = 2
ROW_COUNTER = 3
ROW_HEADER  = 4
ROW_DATA    = 5    # first data row

# WEEK PLAN
WP_TASK_START = 5
WP_TASK_END   = 35
COL_TASK      = 2   # B
COL_DAY       = 4   # D
COL_START     = 5   # E — number_format "HH:MM"
COL_DURATION  = 6   # F — number_format '0.0"h"'
COL_STATUS    = 8   # H — dropdown

# ARCHIVE
ARC_LIVE_ROW   = 5
ARC_FREEZE_ROW = 6
ARC_NUM_COLS   = 11

# TIME GRID
TG_HOUR_START  = 6
TG_ROW_START   = 5
TG_ROW_END     = 22
TG_COL_START   = 2   # B (Sat)
TG_COL_END     = 8   # H (Fri)
DAY_TO_COL     = {"Sat":2,"Sun":3,"Mon":4,"Tue":5,"Wed":6,"Thu":7,"Fri":8}
```
