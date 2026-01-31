---
name: logic-explainer
description: Adds plain-English summaries to complex code blocks.
---
# Skill: Logic Explainer 💡

## Description
Use this skill to add high-level, plain-English summaries to complex blocks of code to improve readability.

## Trigger Criteria
- **Length:** Functions or methods > 15 lines. 📏
- **Depth:** Any code block with ≥ 2 levels of nesting (e.g., nested loops/conditionals). 🪆

## Instructions
1. **Scan:** Analyze the active file for blocks meeting the length or depth criteria.
2. **Draft:** Create a `# LOGIC SUMMARY:` comment block.
3. **Explain:** Describe the "what" and "why" of the logic in 1-2 simple sentences. 
4. **Refine:** Avoid using specific variable names; focus on the business logic or intent.

## Suggestions Logic
- **Context:** When the user is editing or discussing a function that meets Trigger Criteria.
- **Action:** Propose a summary rather than applying it immediately.
- **Dialogue Template:** "I noticed this logic is getting a bit complex. Would you like me to add a plain-English # LOGIC SUMMARY to help keep this readable?"