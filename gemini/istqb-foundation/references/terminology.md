# ISTQB FL — Terminology Quick Reference

## Core Concepts (Ch1)

| Term | Definition | Exam trap |
|------|-----------|-----------|
| **Error** | Human mistake that produces incorrect code | Error → Defect → Failure (order matters) |
| **Defect / Bug / Fault** | Flaw in a work product | Not all defects cause failures |
| **Failure** | Observable incorrect behavior at runtime | External (user sees it) |
| **Root Cause** | Fundamental reason why a defect was introduced | Not the same as the defect itself |
| **Test Basis** | Artifact tests are derived from | Requirements, design docs, code, risk analysis |
| **Test Condition** | Testable aspect of a component or system | Derived from test basis |
| **Test Case** | Set of preconditions, inputs, actions, expected results | Most formal test documentation |
| **Test Procedure** | Sequence of test cases in execution order | How to run them |
| **Test Suite** | Set of test cases/scripts for a component | A collection |
| **Test Oracle** | Source determining expected results | Spec, algorithm, comparable product |
| **Coverage** | Degree to which test criteria have been satisfied | Always expressed as % |
| **Regression Testing** | Testing after change to detect regressions | Prime automation candidate |
| **Confirmation Testing** | Re-testing after defect fix | Also called re-testing |

## Test Activities (Ch1 — Test Process)

| Activity | Key tasks |
|---------|-----------|
| **Test Planning** | Define objectives, approach, resources, schedule, risk |
| **Test Monitoring & Control** | Track progress, take corrective action |
| **Test Analysis** | What to test — identify test conditions from test basis |
| **Test Design** | How to test — design test cases and test data |
| **Test Implementation** | Build the test suite — write scripts, set up environment |
| **Test Execution** | Run tests, log results, compare actual vs expected |
| **Test Completion** | Archive artifacts, report, lessons learned |

## Test Levels (Ch2)

| Level | Also called | Tests | Who |
|-------|------------|-------|-----|
| Component Testing | Unit Testing | Individual units in isolation | Developer |
| Integration Testing | Component integration | Interactions between components | Dev or tester |
| System Testing | End-to-end | Whole system vs requirements | Independent tester |
| Acceptance Testing | UAT | System meets user/business needs | Customer/user |

## Test Types (Ch2)

| Type | Tests what |
|------|-----------|
| **Functional** | What the system does (features, behavior) |
| **Non-functional** | How well it does it (performance, security, usability) |
| **White-box** | Internal structure (code paths, coverage) |
| **Change-related** | Confirmation (re-test) + Regression |

## Static Testing Terms (Ch3)

| Term | Definition |
|------|-----------|
| **Review** | Manual examination of work products (not executing) |
| **Static Analysis** | Tool-based analysis without execution (linters, etc.) |
| **Walkthrough** | Author leads team through document; informal |
| **Technical Review** | Peers review for technical correctness; formal |
| **Inspection** | Most formal review; defined roles, entry/exit criteria, metrics |
| **Anomaly** | Anything deviating from expected; found during review |

## Test Management Terms (Ch5)

| Term | Definition |
|------|-----------|
| **Risk** | Factor that could result in negative outcome; = likelihood × impact |
| **Risk-based testing** | Prioritize test effort based on risk level |
| **Product risk** | Risk that software may fail to meet needs |
| **Project risk** | Risk to the testing project (resources, schedule) |
| **Defect report** | Document describing a failure and its context |
| **Test progress report** | Periodic status of testing (% done, defects found) |
| **Test summary report** | Final report at end of test activity |
| **Entry criteria** | Conditions that must be met before testing starts |
| **Exit criteria** | Conditions that must be met to consider testing done |
| **Test estimation** | Predicting effort needed for testing |

## Commonly Confused Pairs (Exam Traps)

| Pair | Distinction |
|------|------------|
| Verification vs Validation | Verification = built it right (spec); Validation = built the right thing (user need) |
| Error vs Defect vs Failure | Error (human) → Defect (in code) → Failure (at runtime) |
| Test Analysis vs Test Design | Analysis = WHAT to test; Design = HOW to test |
| Regression vs Confirmation | Confirmation = test the fixed bug; Regression = test nothing else broke |
| Statement vs Branch coverage | Branch subsumes statement — 100% branch → 100% statement (not vice versa) |
| Functional vs Non-functional | Functional = features/behavior; Non-functional = quality characteristics |
| Black-box vs White-box | Black = no code knowledge needed; White = tests internal structure |
