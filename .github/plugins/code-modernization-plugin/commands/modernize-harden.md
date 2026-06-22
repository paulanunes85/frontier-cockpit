---
description: Security vulnerability scan + remediation — OWASP, CVE, secrets, injection
argument-hint: <system-dir>
---

Run a **security hardening pass** on `legacy/$1`: find vulnerabilities, rank
them, and fix the critical ones.

## Scan

Spawn the **security-auditor** subagent:

"Adversarially audit legacy/$1 for security vulnerabilities. Cover:
OWASP Top 10 (injection, broken auth, XSS, SSRF, etc.), hardcoded secrets,
vulnerable dependency versions (check package manifests against known CVEs),
missing input validation, insecure deserialization, path traversal.
For each finding return: CWE ID, severity (Critical/High/Med/Low), file:line,
one-sentence exploit scenario, and recommended fix. Also run any available
SAST tooling (npm audit, pip-audit, OWASP dependency-check) and include
its raw output."

## Triage

Write `analysis/$1/SECURITY_FINDINGS.md`:
- Summary scorecard (count by severity, top CWE categories)
- Findings table sorted by severity
- Dependency CVE table (package, installed version, CVE, fixed version)

## Remediate

For each **Critical** and **High** finding, fix it directly in the source.
Make minimal, targeted changes. After each fix, add a one-line entry under
"Remediation Log" in SECURITY_FINDINGS.md: finding ID → commit-style summary
of what changed.

Show the cumulative diff:
```bash
git -C legacy/$1 diff
```

## Verify

Re-run the security-auditor against the patched code to confirm the
Critical/High findings are resolved. Update the scorecard with before/after.

Suggest: `glow -p analysis/$1/SECURITY_FINDINGS.md`
