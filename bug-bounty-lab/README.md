# Bug Bounty Lab Harness

This repository contains controlled, synthetic assets for authorized bug bounty research.

Authorized research targets:

- OpenAI Safety Bug Bounty: https://openai.com/index/safety-bug-bounty/
- GitHub Bug Bounty: https://bounty.github.com/

Rules for this lab:

- Use only accounts, repositories, apps, packages, and documents owned by the researcher.
- Do not include real secrets, personal data, customer data, or third-party data.
- Use synthetic markers only, such as `BB_MARKER_ATLAS_HUB_2026_05_17_A`.
- Do not run high-volume automation, denial-of-service tests, phishing, spam, or social engineering.
- Upload evidence directly to the official bounty platform if a valid issue is found.

Lab files:

- `openai-indirect-prompt-injection-canary.md`: benign attacker-controlled content for testing whether an agent treats untrusted content as instructions.
- `github-authz-matrix.md`: tracking sheet for GitHub-owned account/repo/org permission tests.
- `report-template.md`: reusable bounty submission template.
