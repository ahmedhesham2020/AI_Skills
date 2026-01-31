# AI Validation Skills Library 🛡️⚙️

This repository contains a collection of `.md` skill files designed to enhance AI-assisted software validation. By cloning these into a local agent's directory, they provide expert-level context for specific testing domains.

## 🚀 Key Modules Included

### 1. Requirements-to-Test (R2T) Pro
- **Goal:** Transform "Shall" statements into structured test cases.
- **Outputs:** Positive/Negative test tables, Traceability Matrices, and Python/CAPL snippets.

### 2. SomeIP-SecOC Specialist
- **Goal:** Validating Secure Onboard Communication (SecOC) over Ethernet.
- **Focus:** 64-bit Freshness Value (FV) monotonicity, full 128-bit MAC integrity, and synchronization recovery.

### 3. Automotive Security Architect
- **Goal:** Adversarial and penetration testing mindset.
- **Focus:** Secure Boot, Marvell Switch PFE (Packet Filtering), and UDS Service 0x27/0x29 logic.

## 💻 Installation
To use these skills locally, clone this repo into your Gemini skills folder:
```bash
# On your work laptop:
mkdir -p ~/.gemini/skills
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO.git](https://github.com/YOUR_USERNAME/YOUR_REPO.git) ~/.gemini/skills
