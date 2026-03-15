# HTML Builder — Shared Design System

Provides the CSS design system, component library, and HTML structural patterns used by all of Ahmed's HTML-generating skills. Always loaded when any skill needs to produce an HTML file.

---

## When It's Used

Automatically applied by:
- `defect-report-writer` — JIRA-ready defect reports
- `bug-triage-assistant` — structured triage reports
- `requirements-to-test-cases` — test case exports
- Any future skill that writes an `.html` file

Also triggered directly by: "generate HTML", "create HTML report", "output as HTML"

---

## What It Provides

### Design Tokens (CSS variables)
```
--accent, --accent-2           Brand purple + cyan
--critical/major/minor/trivial Severity colors
--high/medium/low              Priority colors
--bg, --card, --card-2, --border  Surfaces
--text, --muted, --link        Typography
```

### Animations
| Name | Effect |
|------|--------|
| `slideDown` | Page header entrance |
| `fadeIn` | Card entrance (staggered) |
| `fadeInLeft` | Side panel entrance |
| `pulse` | Severity badges (continuous) |
| `growBar` | Progress/risk bars |
| `shimmer` | Loading states |

### Components
| Component | Class Pattern |
|-----------|--------------|
| Cards | `.card`, `.card--accent`, `.card--critical` |
| Grid | `.grid-2`, `.grid-3`, `.grid-4`, `.full-width` |
| Tables | `thead th` / `tbody td` / `td.label` |
| Severity badges | `.badge .badge--[critical\|major\|minor\|trivial\|pass\|fail]` |
| Priority tags | `.tag .tag--[high\|medium\|low\|done\|blocked\|needed\|helpful\|optional]` |
| Domain pill | `.domain-pill .domain-pill--[automotive\|web\|mixed\|general]` |
| Progress bar | `.bar-track` + `.bar-fill .bar-fill--[high\|medium\|low]` |
| Numbered steps | `.steps` (auto-numbered with purple circles) |
| Checklist | `.checklist` + `.check-box` |
| Icon list | `.icon-list` + `data-icon="⚡"` |
| Hypotheses | `.hypothesis .hypothesis--[high\|medium\|low]` |
| Action buckets | `.action-bucket .action-bucket--[immediate\|investigate\|verify]` |
| Stat/KPI cards | `.stat-card .stat-card--[accent\|pass\|fail\|warn]` |
| Timeline | `.timeline` |
| Banner | `.banner` |
| Footer | `.page-footer` |

---

## File Structure

```
~/.claude/skills/html-builder/
├── SKILL.md     ← Full design system + component library
└── README.md    ← This file
```

---

## Design Principles

- **Dark theme only** — `#0f1117` background, never white/light
- **Self-contained** — all CSS inline, no CDN, no external fonts
- **Animated** — every element has an entry animation
- **Consistent** — same tokens, same classes, same look across all reports
