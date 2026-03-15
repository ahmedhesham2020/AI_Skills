# Defect Report Writer — Skill Reference

A Claude Code skill that converts raw defect observations into fully structured, JIRA-ready defect reports. Supports both general QA and automotive embedded contexts.

---

## Trigger

```
/defect-report-writer [raw observation + optional context]
```

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Raw observation | **Yes** | Plain text describing what went wrong |
| Environment | No | testbench / CI / local / HIL / staging |
| Software version | No | Build number, git hash, or version tag |
| Test setup | No | Framework or tool used (pytest, CANoe, manual) |
| Protocol / Module name | No | UDS, SecOC, SOME/IP, login module, payment API, etc. |

---

## Outputs

A clean markdown defect report containing:

| Field | Notes |
|-------|-------|
| Defect ID | Auto-generated format: `DEF-2026-XXX` |
| Defect Title | `Module/Feature: What went wrong` format |
| Severity + Justification | Critical / Major / Minor / Trivial with 1-sentence reason |
| Priority | High / Medium / Low |
| Affected Module | Extracted from input |
| Environment & Setup | All context fields in a table |
| Steps to Reproduce | Numbered, written for a stranger |
| Expected Result | From spec/standard perspective |
| Actual Result | Exact failure behavior |
| Root Cause Hypothesis | Labeled as hypothesis, never stated as fact |
| Suggested Assignee Role | Developer / Security Engineer / Integration Engineer / QA Automation |
| Attachments Needed | Specific file types and names, not generic |
| Pre-JIRA Checklist | Submission quality gate |

### Automotive Bonus Fields (auto-activated)

When automotive keywords are detected (UDS, SecOC, SOME/IP, CAN, Ethernet, HSM, CAPL, CANoe, DoIP, ECU, AUTOSAR, DID, SID, NRC, CMAC, PDU, signal, etc.):

| Extra Field | Notes |
|-------------|-------|
| ECU Variant | e.g., BCM_v2, GW_ECU |
| Communication Protocol | e.g., UDS over CAN |
| Diagnostic Session | Default / Extended / Programming |
| Trace File Reference | .blf / .asc / .pcap filename |
| CANoe / CAPL Version | If applicable |
| Relevant DID / SID / NRC | e.g., SID 0x27, NRC 0x35 |

---

## Example Usage

### General QA (web/API)

```
/defect-report-writer
The login endpoint returns HTTP 200 with an empty user object when
invalid credentials are submitted instead of returning HTTP 401.
Environment: staging. SW version: v2.4.1. Test setup: pytest + requests.
```

**→ Output:** Major severity, High priority, report with Auth Module title,
steps for invalid login flow, expected 401 vs actual 200, hypothesis about
missing credential validation.

---

### Automotive — UDS

```
/defect-report-writer
UDS authentication returns NRC 0x35 instead of providing a seed when
sending SID 0x27 SubFunction 0x01 in extended diagnostic session.
ECU: BCM_v2. SW: build_20260314. Setup: CANoe 17 + CAPL script.
```

**→ Output:** Critical severity, High priority, full automotive report with
ECU Variant, Protocol (UDS over CAN), Diagnostic Session (Extended),
Trace File Reference field, SID/NRC table, and automotive pre-JIRA checklist.

---

### SecOC

```
/defect-report-writer
SecOC verification fails intermittently on CAN frames from the BCM.
CMAC check returns AUTH_FAILED even when freshness counter is in sync.
Testbench setup. CANoe 17. AUTOSAR R21-11.
```

**→ Output:** Major severity, automotive mode active, SecOC + CMAC +
freshness counter fields populated, Security Engineer as assignee.

---

## File Structure

```
~/.claude/skills/defect-report-writer/
├── SKILL.md     ← Main skill definition (loaded by Claude)
└── README.md    ← This file (human reference)
```

---

## Notes

- Output is pure markdown — paste directly into JIRA's Description field
- All unknown fields are filled with `unknown` or `not provided`, never left blank
- Fields that need clarification are tagged `[NEEDS CLARIFICATION]` with an explanation
- Automotive mode activates automatically — no flag needed
