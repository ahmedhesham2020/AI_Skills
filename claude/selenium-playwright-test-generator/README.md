# Selenium / Playwright Test Generator — Skill Reference

Generates a complete, ready-to-run POM-based test automation suite from a plain English
user flow description. Supports both Selenium+Pytest and Playwright+pytest-playwright.

---

## Trigger

```
/selenium-playwright-test-generator [user flow description]
```

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| User flow / scenario | **Yes** | Plain English description of what to test |
| Target URL | No | Base URL of the application under test |
| Browser | No | chromium / firefox / webkit / chrome (default: chromium) |
| Framework | No | Selenium+Pytest or Playwright (default: Playwright) |
| Locators / hints | No | CSS selectors, IDs, aria labels if known |
| Test data hints | No | Usernames, expected values, form data |

---

## Outputs

| File | Description |
|------|-------------|
| `conftest.py` | Driver/browser fixtures, teardown, shared test data |
| `pages/base_page.py` | Shared wait/action helpers all page classes inherit |
| `pages/<name>_page.py` | One page class per page — locators + action methods |
| `tests/test_<scenario>.py` | Test functions with Arrange/Act/Assert structure |
| `requirements.txt` | All dependencies pinned |
| `.gitlab-ci.yml` | install → test → report pipeline |

---

## Design Rules (always applied)

- Page Object Model — locators in page classes, never in test functions
- No `time.sleep()` — `WebDriverWait` for Selenium, auto-wait for Playwright
- No hardcoded test data — fixtures only
- No implicit waits — explicit waits only (Selenium)
- Each test is independently runnable — no shared state between tests

---

## Example Usage

### Playwright (default)

```
/selenium-playwright-test-generator
User flow: A user visits the login page, enters valid credentials, clicks Login,
and lands on the dashboard showing their username in the top-right corner.
URL: https://myapp.example.com
Framework: Playwright
```

**→ Generates:** `LoginPage`, `DashboardPage`, `test_login_valid_credentials`,
cross-browser parametrize fixture, network interception example, GitLab CI pipeline.

---

### Selenium

```
/selenium-playwright-test-generator
User flow: User searches for "laptop" on the e-commerce site, filters by brand "Dell",
and verifies at least one result appears with price under $1000.
URL: https://shop.example.com
Framework: Selenium
Browser: firefox
```

**→ Generates:** `SearchPage`, `ResultsPage`, `test_search_and_filter`,
explicit waits only, headless Firefox config, HTML report stage in CI.

---

## File Structure

```
~/.claude/skills/selenium-playwright-test-generator/
├── SKILL.md     ← Main skill definition
└── README.md    ← This file
```
