---
name: security-sentinel
description: Detects common security vulnerabilities like hardcoded secrets.
---
# Skill: Security Sentinel 🛡️

## Description
Detects common security vulnerabilities (like hardcoded secrets or unsafe inputs) and suggests safer alternatives.

## Trigger Criteria
- **Patterns:** Detecting strings like `API_KEY`, `PASSWORD`, or `SECRET`.
- **Functions:** Use of unsafe functions (e.g., `eval()`, `exec()`, or raw SQL queries).

## Instructions
1. **Audit:** Identify any hardcoded credentials or dangerous function calls.
2. **Warn:** Proactively alert the user about the specific risk (e.g., "Hardcoded keys can be leaked in version control").
3. **Remedy:** Suggest using environment variables or parameterized queries instead.

## Suggestions Logic
- **Context:** When the user enters code containing high-risk strings or functions.
- **Action:** Alert the user to the specific line and offer a fix.
- **Dialogue Template:** "I've detected a potential security risk here. Would you like me to help you move this to an environment variable or use a safer function?"