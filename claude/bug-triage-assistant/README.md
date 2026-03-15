# Bug Triage Assistant — Skill Reference

Performs structured bug triage from a raw observation. Outputs severity, priority, root cause hypotheses, recommended actions, regression risk, and domain-specific fields — as a self-contained animated HTML file.

---

## Trigger

```
/bug-triage-assistant [raw bug observation]
```

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Raw observation | **Yes** | Plain English: what went wrong, what was expected |
| Environment | No | Testbench, CI, HIL, local, staging, production |
| Software version | No | Build number, commit hash, SW version string |
| Test setup | No | Tool chain: CANoe, pytest, Playwright, manual |
| Protocol / Module | No | Auto-detected from keywords |

---

## Domain Auto-Detection

| Domain | Trigger Keywords |
|--------|-----------------|
| **Automotive** | UDS, SecOC, SOME/IP, CAN, Ethernet, HSM, CAPL, CANoe, ECU, AUTOSAR, DTC, ASIL, DID, NRC, PDU |
| **Web/App** | browser, API, HTTP, REST, JSON, UI, login, session, JWT, React, Playwright, Selenium, console error |
| **Mixed** | Both sets detected |
| **General** | Neither set |

---

## Output

A self-contained HTML triage report (`bug_triage_YYYYMMDD_module.html`) containing:

| Section | Content |
|---------|---------|
| Executive Summary | One-sentence boardroom-ready summary |
| Severity Badge | 🔴 Critical / 🟠 Major / 🟡 Minor / 🟢 Trivial (animated pulse) |
| Priority Tag | 🔺 High / 🔸 Medium / 🔹 Low |
| Classification | Module, assignee role, defect ID |
| Environment | SW version, test setup, platform |
| Domain Fields | Automotive (ECU, DTC, CANoe) OR Web/App (browser, endpoint, status code) |
| Steps to Reproduce | Numbered, stranger-reproducible |
| Expected vs Actual | Color-coded (green / red) |
| Root Cause Hypotheses | 2–3 ranked with confidence level + confirm action |
| Recommended Actions | Immediate / Investigation / Fix Verification buckets |
| Regression Risk | Animated risk bar + ripple effects list |
| Attachments Checklist | Specific file types needed |
| Missing Information | Tagged NEEDED / HELPFUL / OPTIONAL |

---

## Example Usage

```
/bug-triage-assistant
During SecOC validation over SOME/IP on the U2A16 platform, the receiver ECU is
accepting messages with an incorrect MAC value instead of rejecting them.
Environment: CANoe 17.0, U2A16 platform, SW Version 2.3.1, AUTOSAR SecOC enabled.
Test Setup: HIL bench, two ECUs over Ethernet, AES-128 MAC truncated to 24 bits.
```

→ Domain: **Automotive** | Severity: 🔴 **Critical** | Priority: 🔺 **High**
→ Writes: `bug_triage_20260315_secoc_mac.html`

---

```
/bug-triage-assistant
Login page returns HTTP 500 on Chrome but works fine on Firefox.
Environment: Staging. SW: v2.1.4. Playwright test suite.
```

→ Domain: **Web/App** | Severity: 🟠 **Major** | Priority: 🔺 **High**
→ Writes: `bug_triage_20260315_login_flow.html`

---

## File Structure

```
~/.claude/skills/bug-triage-assistant/
├── SKILL.md     ← Main skill definition
└── README.md    ← This file
```
