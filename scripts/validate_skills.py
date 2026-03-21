"""
validate_skills.py — CI validator for the AI_Skills repository.

Checks performed on every push:
  1. Dual-format parity    — every claude/[skill] has a gemini/[skill]
  2. Frontmatter fields    — every SKILL.md has name: and description:
  3. Gemini version rule   — gemini SKILL.md must NOT contain version:
  4. README coverage       — every claude skill is mentioned in README.md
  5. Evals integrity       — any evals/evals.json is valid JSON with required keys

Exit 0 if all checks pass, exit 1 if any fail.
"""

import os
import sys
import json
import re

REPO_ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAUDE_DIR  = os.path.join(REPO_ROOT, "claude")
GEMINI_DIR  = os.path.join(REPO_ROOT, "gemini")
README_PATH = os.path.join(REPO_ROOT, "README.md")

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"

errors   = []
warnings = []


def error(msg):
    errors.append(msg)
    print(f"  {FAIL} {msg}")


def ok(msg):
    print(f"  {PASS} {msg}")


def get_skills(base_dir):
    """Return sorted list of skill folder names inside base_dir."""
    if not os.path.isdir(base_dir):
        return []
    return sorted(
        d for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d)) and not d.startswith(".")
    )


def parse_frontmatter(skill_md_path):
    """Extract YAML frontmatter fields from a SKILL.md file.
    Returns a dict of key→value for lines inside the --- delimiters.
    """
    fields = {}
    try:
        with open(skill_md_path, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return fields

    # Match content between the first pair of --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return fields

    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()

    return fields


def check_dual_format(claude_skills, gemini_skills):
    """1. Every claude skill must have a gemini counterpart."""
    print("\n[1] Dual-format parity (claude/ ↔ gemini/)")
    gemini_set = set(gemini_skills)
    all_ok = True
    for skill in claude_skills:
        if skill in gemini_set:
            ok(f"{skill}")
        else:
            error(f"{skill} — missing gemini/{skill}/")
            all_ok = False

    # Also flag gemini-only skills (orphans)
    claude_set = set(claude_skills)
    for skill in gemini_skills:
        if skill not in claude_set:
            error(f"{skill} — gemini/{skill}/ exists but claude/{skill}/ is missing")
            all_ok = False

    if all_ok:
        print(f"  → All {len(claude_skills)} skills have both formats")


def check_frontmatter(claude_skills, gemini_skills):
    """2. Every SKILL.md must have name: and description:.
       3. Gemini SKILL.md must NOT have version:.
    """
    print("\n[2] Frontmatter fields — claude/ (name + description + version)")
    for skill in claude_skills:
        path = os.path.join(CLAUDE_DIR, skill, "SKILL.md")
        if not os.path.exists(path):
            error(f"{skill}/SKILL.md — file missing")
            continue
        fm = parse_frontmatter(path)
        missing = [f for f in ("name", "description", "version") if f not in fm]
        if missing:
            error(f"{skill}/SKILL.md — missing fields: {', '.join(missing)}")
        else:
            ok(f"{skill} — name ✓  description ✓  version ✓")

    print("\n[3] Frontmatter fields — gemini/ (name + description, NO version)")
    for skill in gemini_skills:
        path = os.path.join(GEMINI_DIR, skill, "SKILL.md")
        if not os.path.exists(path):
            error(f"gemini/{skill}/SKILL.md — file missing")
            continue
        fm = parse_frontmatter(path)
        issues = []
        if "name" not in fm:
            issues.append("missing name:")
        if "description" not in fm:
            issues.append("missing description:")
        if "version" in fm:
            issues.append("must NOT contain version: (Gemini rule)")
        if issues:
            error(f"gemini/{skill}/SKILL.md — {', '.join(issues)}")
        else:
            ok(f"gemini/{skill} — name ✓  description ✓  no version ✓")


def check_readme_coverage(claude_skills):
    """4. Every claude skill must be mentioned in README.md."""
    print("\n[4] README.md coverage")
    if not os.path.exists(README_PATH):
        error("README.md not found at repo root")
        return

    with open(README_PATH, encoding="utf-8") as f:
        readme = f.read().lower()

    for skill in claude_skills:
        slug = skill.lower()
        slug_spaced = slug.replace("-", " ")

        # Primary check: full slug or spaced version
        if slug in readme or slug_spaced in readme:
            ok(f"{skill}")
            continue

        # Fallback: check meaningful tokens (5+ chars) against README,
        # also against a hyphen-stripped version of the README to handle
        # "Co-authoring" matching "coauthoring", etc.
        readme_nohyphen = readme.replace("-", "")
        tokens = [t for t in slug.split("-") if len(t) >= 5]
        if tokens and any(t in readme or t in readme_nohyphen for t in tokens):
            ok(f"{skill}")
        else:
            error(f"{skill} — not mentioned in README.md")


def check_evals(claude_skills):
    """5. Any evals/evals.json must be valid JSON with required keys."""
    print("\n[5] Evals integrity (evals/evals.json)")
    found_any = False
    for skill in claude_skills:
        evals_path = os.path.join(CLAUDE_DIR, skill, "evals", "evals.json")
        if not os.path.exists(evals_path):
            continue
        found_any = True
        try:
            with open(evals_path, encoding="utf-8") as f:
                data = json.load(f)
            # Check top-level keys
            if "skill_name" not in data or "evals" not in data:
                error(f"{skill}/evals/evals.json — missing 'skill_name' or 'evals' key")
                continue
            # Check each eval entry
            entry_errors = []
            for i, entry in enumerate(data["evals"]):
                for key in ("id", "prompt", "expected_output"):
                    if key not in entry:
                        entry_errors.append(f"entry {i} missing '{key}'")
            if entry_errors:
                error(f"{skill}/evals/evals.json — {'; '.join(entry_errors)}")
            else:
                ok(f"{skill} — {len(data['evals'])} eval(s) valid")
        except json.JSONDecodeError as e:
            error(f"{skill}/evals/evals.json — invalid JSON: {e}")

    if not found_any:
        print("  (no evals.json files found — skipped)")


def main():
    print("=" * 55)
    print("  AI Skills Repository — Validation")
    print("=" * 55)

    claude_skills = get_skills(CLAUDE_DIR)
    gemini_skills = get_skills(GEMINI_DIR)

    print(f"\nFound {len(claude_skills)} claude skills, {len(gemini_skills)} gemini skills")

    check_dual_format(claude_skills, gemini_skills)
    check_frontmatter(claude_skills, gemini_skills)
    check_readme_coverage(claude_skills)
    check_evals(claude_skills)

    print("\n" + "=" * 55)
    if errors:
        print(f"  FAILED — {len(errors)} error(s) found:\n")
        for i, e in enumerate(errors, 1):
            print(f"    {i}. {e}")
        print()
        sys.exit(1)
    else:
        print(f"  PASSED — all checks clean ({len(claude_skills)} skills validated)")
        print("=" * 55)
        sys.exit(0)


if __name__ == "__main__":
    main()
