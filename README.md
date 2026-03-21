# AI Skills Library

A collection of Claude Code skill files for software validation, test automation, and engineering productivity. Clone into your Claude skills directory to activate expert-level context for each domain.

## Installation

### Claude Code
```bash
# Copy skills into your Claude skills folder
cp -r claude/* ~/.claude/skills/
```

### Gemini CLI
```bash
# Link skills into your Gemini skills folder
gemini skills link /path/to/03-AI_Skills/gemini
# or copy manually
cp -r gemini/* ~/.gemini/skills/
```

---

## Skills

### 1. Requirements-to-Test-Cases
- **Goal:** Transform any plain-text software requirement into a complete, structured test case document.
- **Domains:** Automotive embedded (UDS/ISO 14229, SecOC, SOME/IP, Secure Boot, AUTOSAR) and Web/API/UI (REST, functional, regression).
- **Outputs:** Summary table + detailed TC breakdown (ID, Title, Preconditions, Steps, Expected Result, Test Type, Priority) + Traceability Matrix. Minimum 1 Positive, 1 Negative, and 1 Boundary test case per requirement. Excel file written to the current working directory.

### 2. CAPL Script Generator
- **Goal:** Generate complete, ready-to-run CAPL scripts for Vector CANoe/CANalyzer from a plain English test scenario.
- **Reference:** Grounded in `references/CAPL_Help.md` — 1,126 entries / 40,183 lines of CAPL documentation scraped from the Vector CANoe 19 help portal. Every function is verified against this reference before output.
- **Supported scenarios:** CAN TX/RX validation, signal boundary monitoring, UDS 0x27/0x29 diagnostic sequences, error frame injection, cycle time validation, SecOC MAC checking.
- **Outputs:** Two files — `[name]_Utils.can` (reusable `testfunction` helpers) + `[name]_Tests.can` (clean `testcase` functions that call into Utils) + companion `_report.md`.

### 3. ISTQB Foundation Level — Applied Testing
- **Goal:** Apply ISTQB FL knowledge to real test design and exam preparation.
- **Modes:** Interactive quiz (Ch1/Ch4/Ch2), test case design using EP/BVA/Decision Table/State Transition, test review, concept explanations with automotive analogies, exam-day checklist.
- **Outputs:** Scored quizzes (Pass/Fail vs 75%), pytest-ready test cases, ISTQB-aligned defect reports.

### 4. Selenium / Playwright Test Generator
- **Goal:** Generate Selenium or Playwright UI test scripts from a user flow description.
- **Pattern:** Always uses Page Object Model (POM) — page classes separated from test classes, no hardcoded test data.
- **Outputs:** Full POM project scaffold with page classes, test classes, and pytest fixtures.

### 5. Defect Report Writer
- **Goal:** Turn a raw defect observation into a structured, JIRA-ready defect report.
- **Domains:** Automotive (UDS, SecOC, SOME/IP, ECU, CANoe) and Web/App (browser, API, UI).
- **Outputs:** Self-contained HTML defect report with animated visuals, ready to attach to a JIRA ticket.

### 6. Bug Triage Assistant
- **Goal:** Triage and classify a bug — severity, root cause hypothesis, regression risk, and recommended actions.
- **Domains:** Automotive embedded and Web/App.
- **Outputs:** Structured triage analysis with severity classification, root cause hypotheses, and next steps.

### 7. GitLab CI Pipeline Builder
- **Goal:** Generate a `.gitlab-ci.yml` pipeline for a test automation project.
- **Supported stacks:** Python + Pytest + Selenium, Python + Pytest + Playwright, Robot Framework, JavaScript + Playwright, mixed stacks.
- **Outputs:** Complete `.gitlab-ci.yml` with stages, lint/test/report jobs, artifact configuration, and caching.

### 8. SOLID Design Principles
- **Goal:** Apply SOLID principles to code review, system design, teaching, and quiz modes.
- **Use when:** User pastes code for review, asks to explain a principle, wants to design a system using SOLID, needs a pre-merge checklist, or wants a quiz on SOLID concepts.
- **Outputs:** Violation table + refactored code (REVIEW), principle explanation with examples (EXPLAIN), class/interface scaffold (APPLY), pass/fail audit (CHECKLIST), or scored quiz (QUIZ).

### 9. Skill Creator
- **Goal:** Scaffold a new Claude Code skill from a description.
- **Outputs:** Complete `SKILL.md` with frontmatter, step-by-step instructions, templates, and output format rules.

### 10. Sub-Agent Creator
- **Goal:** Create custom sub-agent definition files for use in multi-agent workflows.
- **Outputs:** Agent definition file with name, description, capabilities, and instructions.

### 11. HTML Builder — Shared Design System
- **Goal:** Provide a consistent design system and CSS component library used across all skills that generate HTML output.
- **Auto-loaded by:** Defect Report Writer, Bug Triage Assistant, Requirements-to-Test-Cases, and any skill that produces an HTML file.
- **Outputs:** Fully styled HTML files using a shared design token system (colors, typography, cards, tables, badges, progress bars) — no custom styles invented per skill.

### 12. Frontend Design
- **Goal:** Create distinctive, production-grade frontend interfaces with high design quality.
- **Use when:** Building web components, pages, dashboards, React components, HTML/CSS layouts, or styling/beautifying any web UI.
- **Outputs:** Polished HTML/CSS/JS or React code that avoids generic AI aesthetics.

### 13. Web Artifacts Builder
- **Goal:** Build elaborate, multi-component web applications using React, Tailwind CSS, and shadcn/ui.
- **Use when:** Complex artifacts requiring state management, routing, or shadcn/ui components are needed.
- **Outputs:** Single-file HTML artifacts with bundled React + Tailwind + shadcn/ui, ready to run in the browser.

### 14. Webapp Testing
- **Goal:** Interact with and test local web applications using Playwright.
- **Use when:** Verifying frontend functionality, debugging UI behavior, capturing screenshots, or viewing browser logs.
- **Outputs:** Test results, screenshots, browser logs, and Playwright automation scripts.

### 15. XLSX
- **Goal:** Create, read, edit, and analyze spreadsheet files (`.xlsx`, `.xlsm`, `.csv`, `.tsv`).
- **Use when:** Any task where a spreadsheet is the primary input or output — formulas, formatting, charting, data cleaning, or format conversion.
- **Outputs:** Fully formatted `.xlsx` files with formulas, charts, and structured data.

### 16. DOCX
- **Goal:** Create, read, edit, and manipulate Word documents (`.docx`).
- **Outputs:** Formatted `.docx` files with tables, headers, images, and table of contents.

### 17. PDF
- **Goal:** Process PDFs — read, extract text/tables, merge, split, rotate, add watermarks, fill forms, OCR.
- **Outputs:** Modified or newly created `.pdf` files.

### 18. PPTX
- **Goal:** Create, read, edit, and manipulate PowerPoint presentations.
- **Outputs:** Polished `.pptx` slide decks with professional design.

### 19. Algorithmic Art
- **Goal:** Create algorithmic and generative art using p5.js with seeded randomness and interactive parameter exploration.
- **Outputs:** `.html` interactive viewer, `.js` algorithm file, `.md` design philosophy.

### 20. Brand Guidelines
- **Goal:** Apply consistent brand colors, typography, and visual identity to artifacts.
- **Outputs:** Styled artifacts using defined brand tokens.

### 21. Canvas Design
- **Goal:** Create beautiful static visual art and design pieces (posters, illustrations).
- **Outputs:** `.pdf`, `.png`, and `.md` design philosophy files.

### 22. Claude API
- **Goal:** Build LLM-powered applications using the Claude API or Anthropic SDKs.
- **Outputs:** Working application code with Claude API integration across Python, TypeScript, and other languages.

### 23. Doc Co-authoring
- **Goal:** Structured workflow for co-authoring technical documentation (specs, proposals, decision docs, RFCs).
- **Outputs:** Professional technical documents with context gathering and reader testing steps.

### 24. Internal Comms
- **Goal:** Write internal communications — status reports, 3P updates, newsletters, FAQs.
- **Outputs:** Structured internal communication documents.

### 25. MCP Builder
- **Goal:** Create high-quality MCP (Model Context Protocol) servers for LLM integration with external services.
- **Outputs:** MCP server with well-designed tools and documentation.

### 26. Skill Creator
- **Goal:** Create new skills, iterate and improve existing skills, run evaluations to test skill performance.
- **Outputs:** New or improved `SKILL.md` files with testing and optimization loops.

### 27. Slack GIF Creator
- **Goal:** Create animated GIFs optimized for Slack (emoji or message GIFs).
- **Outputs:** `.gif` files optimized for Slack constraints (128×128 or 480×480).

### 28. Theme Factory
- **Goal:** Apply professional font and color themes to artifacts — 10 presets plus custom.
- **Outputs:** Consistently themed presentations, documents, and web artifacts.

### 29. Learning Mentor
- **Goal:** Search the web for a current learning roadmap on any topic, filter it through the Pareto principle, and guide the user interactively from beginner to expert one session at a time.
- **Use when:** User says "teach me", "I want to learn", "mentor me on", "roadmap for", or provides any topic name and asks to start learning it.
- **Outputs:** Pareto-filtered learning plan (Core 20% + Bonus sessions) + interactive session-by-session mentorship with exercises, feedback, and a bonus unlock gate.

### 30. Visual Planner
- **Goal:** Search the web + use LLM knowledge to build a milestone roadmap for any goal, then generate a self-contained interactive HTML tracking dashboard.
- **Use when:** User says "create a plan for", "build a roadmap for", "I need a plan to", "make a visual plan", or describes any goal and asks for milestones.
- **Outputs:** Interactive HTML file with circular SVG progress rings per phase, clickable milestone checkboxes, live overall progress bar, and localStorage persistence — works offline in any browser.

### 31. Prompt Architect
- **Goal:** Transform a rough user request into a complete, structured prompt using a six-section anatomy (Role, Task, Context Block, Goal/Stakes, Completion Criteria, Output Format).
- **Use when:** You want a high-quality, copy-ready prompt for any task — launches, plans, audits, test suites, study plans, and more. Asks 3 clarifying questions if input is too thin.
- **Outputs:** A fenced, copy-ready prompt with all 6 labeled sections + a quality check summary + one improvement tip.

### 32. System Architect
- **Goal:** Design and build any operational system — attendance, goal-tracking, HR, project management, lifestyle, OKR, CRM, and more — grounded in core architectural principles (scalability, CAP theorem, fault tolerance, security by design).
- **Use when:** User says "build me a system for", "design a system that tracks", "I need a system to manage", "create an attendance system", "make a goal tracker", or describes any structured operational tool they need.
- **Outputs:** Personal/team scale → interactive HTML dashboard + Excel workbook (with visuals, trackers, progress rings, charts, branded). Enterprise scale → architecture document with tool recommendations, system data model, component map, and five-pillar architectural principles analysis.

### 33. Automation Engineer
- **Goal:** Build complete, production-ready automated systems for any manual or repetitive business process — scripts, schedulers, integrations, error handlers, notifications, and dashboards.
- **Use when:** User says "automate this process", "we do this manually every day", "build a workflow that", "stop doing X manually", "save time on", or describes any multi-step manual task done repeatedly by staff.
- **Outputs:** Working code for all components + 7-page deployment PDF guide (visual architecture diagram, prerequisites, step-by-step deployment, verification checklist, rollback plan) + executed test results (T-01 happy path, T-02 failure/recovery, T-03 security) + Automation Delivery Report with architecture decisions, estimated savings with calculation, and go-live checklist.

### 34. Project Tracker
- **Goal:** Resume and drive forward any software project tracked in a markdown file — no manual prompt pasting needed.
- **Use when:** User says "/project-tracker", "resume my project", "continue my project", "where did I leave off", "what's my next step", or "pick up where we stopped". Also triggers on "let's keep working" or "what was I doing last time" at the start of a session.
- **Outputs:** Orientation briefing (active project, last step, next step, checklist progress) + completed work for the next step + updated markdown file (checkboxes, Last Step, Next Step, Status, Session Log) after every completed step.

### 35. Life Systems Builder
- **Goal:** Build a complete personal productivity system for any life area using the Ali Abdaal (enjoyable, sustainable) and Leila Hormozi (tight, operational) frameworks.
- **Use when:** User says "help me build a system for", "I scored X/10 in", "I keep failing at [area]", "make this systematic", or describes any life area they want to improve with structure.
- **Outputs:** Identity vision + SOP (Trigger/Tool/Time per step) + default weekly schedule + 3 lead indicators + 30-day kickstart plan + one automation opportunity.

### 36. Excel Planner Builder
- **Goal:** Build a complete Excel/Google Sheets planner or tracker from a plain description — Python openpyxl generator + Google Apps Script automation file.
- **Use when:** User says "create a tracker", "build a planner", "I need an Excel for", "make a weekly plan", "build me a dashboard", "I need a Google Sheets template", or describes any system they want to manage in a spreadsheet.
- **Outputs:** `generate_<name>.py` (fully styled Excel file with nav bar, dropdowns, conditional formatting, progress bars, charts) + `<name>_sync.gs` (live onEdit sync, cell merging, scheduled resets, custom menu).
