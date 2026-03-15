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
- **Goal:** Apply SOLID principles to system and code design.
- **Outputs:** Guided design review, refactoring suggestions, and examples following Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles.

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
