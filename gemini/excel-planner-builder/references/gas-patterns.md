# Google Apps Script Patterns

Complete, copy-paste-ready patterns for every automation scenario. Use these verbatim — do not rewrite from scratch.

---

## Critical Rules (never break these)

1. **Never use `getHours()`** for time comparisons. Google Sheets stores time values as Date objects in UTC (e.g., 9:00 AM in a UTC+3 sheet is stored as `1899-12-30T06:00:00.000Z`). Using `getHours()` returns the UTC hour, not the local hour. Always use `toMs_()` which compares raw millisecond values from `.getTime()` — both sides go through the same function so timezone is irrelevant.

2. **Always `breakApart()` before merging.** If you call `mergeVertically()` on a range that contains already-merged cells, Apps Script throws an error. Call `tgSheet.getRange(...).breakApart()` on the full region at the start of every sync pass.

3. **No UI in scheduled functions.** `SpreadsheetApp.getUi()` throws when called from a time-based trigger (no screen context). Use `Logger.log()` in scheduled functions. Only call `getUi()` in manually-triggered functions.

4. **One trigger per function.** `createArchiveTrigger()` always calls `deleteArchiveTrigger()` first to remove any existing trigger before creating a new one. Prevents duplicate triggers building up.

---

## Custom Menu

```javascript
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Weekly Tools')
    .addItem('Sync TIME GRID now', 'syncNow')
    .addSeparator()
    .addItem('Archive This Week  (manual)', 'archiveWeek')
    .addSeparator()
    .addItem('Set up Saturday 12 PM auto-archive', 'createArchiveTrigger')
    .addItem('Remove Saturday auto-archive',        'deleteArchiveTrigger')
    .addToUi();
}
```

---

## onEdit Trigger

```javascript
// Fires automatically on every cell edit — no authorization needed (simple trigger).
// Only acts when edits happen in the relevant sheet and columns.
function onEdit(e) {
  if (!e) return;
  const sheet = e.range.getSheet();
  if (sheet.getName() !== 'WEEK PLAN') return;
  const col = e.range.getColumn();
  // COL_TASK=2, COL_DURATION=6 — adjust to match your layout
  if (col >= 2 && col <= 6) {
    syncTimeGrid_();
  }
}

function syncNow() {
  syncTimeGrid_();
  Logger.log('Done.');
}
```

---

## Timezone-Safe Time Helper

```javascript
/**
 * Convert any Google Sheets time cell value to milliseconds.
 * Works by reading the raw .getTime() from Date objects — never uses
 * getHours() — so timezone offsets cannot cause slot mismatches.
 *
 * Google Sheets stores time values as Date objects anchored to
 * 1899-12-30 + the time offset in UTC. Both task times and TIME GRID
 * slot times go through this same function, so comparisons are always
 * consistent regardless of the spreadsheet's timezone.
 */
function toMs_(value) {
  if (value === null || value === undefined || value === '') return null;

  if (value instanceof Date) {
    const ms = value.getTime();
    // Empty time-formatted cell = Sheets epoch midnight (1899-12-30T00:00:00Z)
    if (ms === new Date('1899-12-30T00:00:00.000Z').getTime()) return null;
    return ms;
  }

  if (typeof value === 'number' && value > 0) {
    // Excel/Sheets serial fraction: days since 1899-12-30
    const EPOCH_MS = new Date('1899-12-30T00:00:00.000Z').getTime();
    return EPOCH_MS + value * 86400000;
  }

  if (typeof value === 'string') {
    const parts = value.trim().split(':');
    if (parts.length >= 2) {
      const h = parseInt(parts[0], 10);
      const m = parseInt(parts[1], 10);
      const EPOCH_MS = new Date('1899-12-30T00:00:00.000Z').getTime();
      return EPOCH_MS + (h * 3600 + m * 60) * 1000;
    }
  }
  return null;
}

/**
 * Parse duration to decimal hours.
 * Accepts: 1.5, "1.5h", "90m", "1:30"
 */
function parseDuration_(value) {
  if (value === null || value === undefined || value === '') return null;
  if (typeof value === 'number') return value > 0 ? value : null;
  if (typeof value === 'string') {
    const v = value.trim().toLowerCase();
    if (!v) return null;
    if (v.endsWith('h'))  return parseFloat(v) || null;
    if (v.endsWith('m'))  return (parseFloat(v) / 60) || null;
    if (v.includes(':')) {
      const p = v.split(':');
      return parseInt(p[0], 10) + parseInt(p[1], 10) / 60;
    }
    return parseFloat(v) || null;
  }
  return null;
}
```

---

## TIME GRID Sync with Cell Merging

```javascript
const ONE_HOUR_MS = 3600000;

// Constants — adjust to match your layout
const TG_FIRST_ROW = 5;   // row 5 = 06:00
const TG_LAST_ROW  = 22;  // row 22 = 23:00
const TG_FIRST_COL = 2;   // col B
const TG_LAST_COL  = 8;   // col H
const DAY_TO_COL   = { Sat:2, Sun:3, Mon:4, Tue:5, Wed:6, Thu:7, Fri:8 };

// Colors
const COLOR_TASK_BG   = '#FFF9E6';
const COLOR_TASK_FT   = '#9C5700';
const COLOR_SAT_EMPTY = '#F2E0FF';
const COLOR_ALT_EMPTY = '#F8F8FF';
const COLOR_WHITE     = '#FFFFFF';
const COLOR_BLACK     = '#000000';

function syncTimeGrid_() {
  const ss      = SpreadsheetApp.getActiveSpreadsheet();
  const wpSheet = ss.getSheetByName('WEEK PLAN');
  const tgSheet = ss.getSheetByName('TIME GRID');
  if (!wpSheet || !tgSheet) return;

  const numRows = TG_LAST_ROW - TG_FIRST_ROW + 1;
  const numCols = TG_LAST_COL - TG_FIRST_COL + 1;

  // Step 1: Read TIME GRID col A slot times as ms
  // This is the key: we read actual cell values — not hardcoded hours.
  const rawSlots = tgSheet.getRange(TG_FIRST_ROW, 1, numRows, 1).getValues();
  const slotMs   = rawSlots.map(r => toMs_(r[0]));

  // Step 2: Read WEEK PLAN task rows
  const numTaskRows = 31; // adjust to your last task row minus first
  const rawTasks = wpSheet.getRange(5, 1, numTaskRows, 6).getValues();

  // Step 3: Build slot map
  // key "col,rowIndex" → [task names]
  const slotMap = {};
  rawTasks.forEach(row => {
    const taskName = row[1]; // col B (0-based = index 1)
    if (!taskName) return;
    const col        = DAY_TO_COL[String(row[3]).trim()]; // col D
    const startMs    = toMs_(row[4]);                     // col E
    const durationMs = parseDuration_(row[5]) * ONE_HOUR_MS; // col F
    if (!col || startMs === null || !durationMs || durationMs <= 0) return;
    const endMs = startMs + durationMs;
    slotMs.forEach((slotStart, i) => {
      if (slotStart === null) return;
      const slotEnd = slotStart + ONE_HOUR_MS;
      // Overlap check: task starts before slot ends AND task ends after slot starts
      if (startMs < slotEnd && endMs > slotStart) {
        const key = col + ',' + i;
        if (!slotMap[key]) slotMap[key] = [];
        slotMap[key].push(String(taskName));
      }
    });
  });

  // Step 4: Unmerge ALL cells first — required before re-merging
  tgSheet.getRange(TG_FIRST_ROW, TG_FIRST_COL, numRows, numCols).breakApart();

  // Step 5: Write column by column, merging consecutive same-task runs
  for (let c = 0; c < numCols; c++) {
    const col = c + TG_FIRST_COL;
    let r = 0;
    while (r < numRows) {
      const key = col + ',' + r;
      if (slotMap[key]) {
        const taskText = slotMap[key].join('\n');
        // Find how many consecutive rows share the same task text
        let runLen = 1;
        while (r + runLen < numRows) {
          const nextKey = col + ',' + (r + runLen);
          if (slotMap[nextKey] && slotMap[nextKey].join('\n') === taskText) {
            runLen++;
          } else break;
        }
        // Merge the run and style it
        const range = tgSheet.getRange(r + TG_FIRST_ROW, col, runLen, 1);
        if (runLen > 1) range.mergeVertically();
        range.setValue(taskText);
        range.setBackground(COLOR_TASK_BG);
        range.setFontWeight('bold');
        range.setFontColor(COLOR_TASK_FT);
        range.setVerticalAlignment('middle');
        range.setHorizontalAlignment('left');
        range.setWrap(true);
        r += runLen;
      } else {
        const row  = r + TG_FIRST_ROW;
        const cell = tgSheet.getRange(row, col);
        const bg   = col === 2 ? COLOR_SAT_EMPTY
                   : (row % 2 === 0 ? COLOR_ALT_EMPTY : COLOR_WHITE);
        cell.setValue('');
        cell.setBackground(bg);
        cell.setFontWeight('normal');
        cell.setFontColor(COLOR_BLACK);
        cell.setVerticalAlignment('middle');
        r++;
      }
    }
  }
  SpreadsheetApp.flush();
}
```

---

## Archive Reset — Manual (with confirmation dialog)

```javascript
// Archive layout constants
const ARC_LIVE_ROW   = 5;
const ARC_FREEZE_ROW = 6;
const ARC_NUM_COLS   = 11;
const ARC_PCT_COL    = 7;

// WEEK PLAN reset constants
const WP_DATE_CELL   = 'K1';
const WP_STATUS_COL  = 8;
const WP_CLEAR_START = 2;
const WP_CLEAR_END   = 9;

// SAT CHECKLIST reset constants
const SAT_DATA_START   = 6;
const SAT_DATA_END     = 21;
const SAT_ANSWER_COL   = 4;
const SAT_STATUS_COL   = 5;
const SAT_DIVIDER_ROWS = [5, 11, 17];

function archiveWeek() {
  const ui = SpreadsheetApp.getUi();
  const confirm = ui.alert(
    'Archive This Week?',
    'This will:\n\n' +
    '  1. Freeze current week into ARCHIVE\n' +
    '  2. Advance week start date by +7 days\n' +
    '  3. Clear all WEEK PLAN tasks\n' +
    '  4. Reset SAT CHECKLIST answers → Pending\n' +
    '  5. Clear TIME GRID\n\n' +
    'Cannot be undone. Proceed?',
    ui.ButtonSet.YES_NO
  );
  if (confirm !== ui.Button.YES) return;

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  runArchive_(ss);

  const newDate = ss.getSheetByName('WEEK PLAN').getRange(WP_DATE_CELL).getValue();
  const newDateStr = Utilities.formatDate(newDate, Session.getScriptTimeZone(), 'dd MMM yyyy');
  ui.alert('Done!',
    'Week archived.\nNew week starts: ' + newDateStr + '\n\n' +
    'Next steps:\n  1. Fill in SAT CHECKLIST\n  2. Add tasks to WEEK PLAN\n  3. TIME GRID auto-updates as you type',
    ui.ButtonSet.OK
  );
}
```

---

## Archive Reset — Scheduled (no UI dialogs)

```javascript
// This is what the time-based trigger calls — no getUi() allowed here.
function archiveWeekAuto_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  runArchive_(ss);
  Logger.log('[archiveWeekAuto_] Done.');
}

// Shared logic used by both manual and scheduled versions
function runArchive_(ss) {
  const arcSheet = ss.getSheetByName('ARCHIVE');
  const wpSheet  = ss.getSheetByName('WEEK PLAN');
  const satSheet = ss.getSheetByName('SAT CHECKLIST');
  const tgSheet  = ss.getSheetByName('TIME GRID');
  if (!arcSheet || !wpSheet || !satSheet || !tgSheet) {
    Logger.log('[runArchive_] ERROR: sheet not found');
    return;
  }

  // Step 1: Read live values from ARCHIVE row 5
  // getValues() returns computed values, not formula strings — exactly what we want.
  const liveValues = arcSheet.getRange(ARC_LIVE_ROW, 1, 1, ARC_NUM_COLS).getValues()[0];

  // Step 2: Insert frozen row at position 6 (pushes history down)
  arcSheet.insertRowBefore(ARC_FREEZE_ROW);
  arcSheet.getRange(ARC_FREEZE_ROW, 1, 1, ARC_NUM_COLS).setValues([liveValues]);
  arcSheet.getRange(ARC_FREEZE_ROW, ARC_PCT_COL).setNumberFormat('0%');

  // Step 3: Advance K1 date by 7 days
  const k1Cell = wpSheet.getRange(WP_DATE_CELL);
  const oldDate = k1Cell.getValue();
  let newDate;
  if (oldDate instanceof Date) {
    newDate = new Date(oldDate.getTime() + 7 * 24 * 3600 * 1000);
  } else {
    const today = new Date();
    const daysUntilSat = (6 - today.getDay() + 7) % 7 || 7;
    newDate = new Date(today.getTime() + daysUntilSat * 24 * 3600 * 1000);
  }
  k1Cell.setValue(newDate);
  k1Cell.setNumberFormat('DD-MMM-YYYY');

  // Step 4: Clear WEEK PLAN tasks
  for (let r = 5; r <= 35; r++) {
    for (let c = WP_CLEAR_START; c <= WP_CLEAR_END; c++) {
      wpSheet.getRange(r, c).setValue(c === WP_STATUS_COL ? 'Not Started' : '');
    }
  }

  // Step 5: Reset SAT CHECKLIST
  for (let r = SAT_DATA_START; r <= SAT_DATA_END; r++) {
    if (SAT_DIVIDER_ROWS.includes(r)) continue;
    satSheet.getRange(r, SAT_ANSWER_COL).setValue('');
    satSheet.getRange(r, SAT_STATUS_COL).setValue('Pending');
  }

  // Step 6: Clear TIME GRID — unmerge first, then clear content
  const tgNumRows = TG_LAST_ROW - TG_FIRST_ROW + 1;
  const tgNumCols = TG_LAST_COL - TG_FIRST_COL + 1;
  const tgRange = tgSheet.getRange(TG_FIRST_ROW, TG_FIRST_COL, tgNumRows, tgNumCols);
  tgRange.breakApart();
  tgRange.clearContent();

  SpreadsheetApp.flush();
}
```

---

## Trigger Management

```javascript
/**
 * Run ONCE from the menu to register the weekly trigger.
 * Removes any existing trigger first to prevent duplicates.
 * Trigger fires every Saturday between 12:00–12:59 in the script's timezone.
 *
 * IMPORTANT: tell the user to verify timezone in
 * Apps Script → Project Settings → Time zone.
 */
function createArchiveTrigger() {
  deleteArchiveTrigger();  // always clean up first

  ScriptApp.newTrigger('archiveWeekAuto_')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.SATURDAY)
    .atHour(12)
    .create();

  SpreadsheetApp.getUi().alert(
    'Saturday trigger set!',
    'archiveWeekAuto_ will run every Saturday at 12:00–12:59.\n\n' +
    'Verify timezone: Apps Script → Project Settings → Time zone.',
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}

function deleteArchiveTrigger() {
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === 'archiveWeekAuto_') {
      ScriptApp.deleteTrigger(t);
    }
  });
}
```

---

## Trigger Day Reference

```javascript
ScriptApp.WeekDay.MONDAY
ScriptApp.WeekDay.TUESDAY
ScriptApp.WeekDay.WEDNESDAY
ScriptApp.WeekDay.THURSDAY
ScriptApp.WeekDay.FRIDAY
ScriptApp.WeekDay.SATURDAY
ScriptApp.WeekDay.SUNDAY
```

---

## Performance Notes

- **Batch writes** (`setValues`, `setBackgrounds`, `setFontWeights`) → use when NOT merging cells. 3 API calls for an 18×7 grid = fast.
- **Individual range calls** → use when merging is needed. Each merged "run" = one `getRange()` + `mergeVertically()` + style calls. For a typical 18×7 grid with ~10 tasks, this is ~30–50 calls = still fast enough.
- **`SpreadsheetApp.flush()`** → always call at the end of a sync. Forces all pending writes to commit before the function returns.
- **`getValues()` vs `getValue()`** → always use `getValues()` to read a range in a single API call. Never read cells one by one in a loop.
