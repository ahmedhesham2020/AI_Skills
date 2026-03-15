# GitLab CI Pipeline Builder — Skill Reference

Generates a complete, production-ready `.gitlab-ci.yml` from a plain English
project description. Minimum viable pipeline first, optional enhancements listed separately.

---

## Trigger

```
/gitlab-ci-pipeline-builder [project description]
```

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Project description | **Yes** | Plain English: what the project does and what tests it runs |
| Programming language | No | Python / JavaScript (default: Python) |
| Test framework | No | Pytest+Selenium / Pytest+Playwright / Robot Framework / JS+Playwright / Mixed |
| Docker image | No | Custom base image (default: matched to stack) |
| Report format | No | pytest-html / allure / robot built-in |
| Deployment target | No | staging / production / none (default: none) |
| Browser | No | chromium / firefox / webkit (default: chromium) |

---

## Supported Stacks

| Stack | Lint tool | Browser install | Report |
|-------|-----------|----------------|--------|
| Python + Pytest + Playwright | flake8 | `playwright install --with-deps` | pytest-html |
| Python + Pytest + Selenium | flake8 | Chrome via apt-get | pytest-html |
| Python + Robot Framework | robocop | Chrome via apt-get | robot built-in |
| JavaScript + Playwright | eslint | `npx playwright install --with-deps` | playwright HTML |
| Mixed Pytest + Robot Framework | flake8 + robocop | both | both |

---

## Output

A `.gitlab-ci.yml` file written to the current working directory containing:

| Block | What it does |
|-------|-------------|
| `stages` | Ordered: install → lint → test → report → deploy (optional) |
| `variables` | Python/Node version, URLs, report paths, cache dirs |
| `cache` | Branch-scoped pip/npm + browser binary cache |
| `install` | venv + pip/npm install + browser download, artifact passed to downstream |
| `lint` | flake8/robocop/eslint — MR only, `allow_failure: false` |
| `test` | Full suite, headless, `retry: 1`, `timeout: 30min`, JUnit XML artifact |
| `report` | Artifact collection, `when: always` |
| `deploy` | Tagged releases only — omitted if no deployment target given |

---

## Example Usage

### Playwright (cross-browser)

```
/gitlab-ci-pipeline-builder
Project: SauceDemo login test suite. Python + Playwright + pytest-playwright.
Cross-browser: Chromium + Firefox. pytest-html reports. No deployment.
```

→ Generates: `install` + `lint` (MR) + `test:chromium` + `test:firefox` (parallel) + `report`

---

### Selenium

```
/gitlab-ci-pipeline-builder
Stack: Python + Selenium + Pytest. Single browser (Chrome headless).
Report: pytest-html. No cross-browser needed.
```

→ Generates: `install` (with Chrome apt-get install) + `lint` + `test` + `report`

---

### Robot Framework

```
/gitlab-ci-pipeline-builder
Stack: Python + Robot Framework + SeleniumLibrary.
Browser: headlesschrome. Output dir: robot_results/.
```

→ Generates: `install` + `lint:robocop` + `test:robot` + `report:rebot`

---

## File Structure

```
~/.claude/skills/gitlab-ci-pipeline-builder/
├── SKILL.md     ← Main skill definition
└── README.md    ← This file
```
