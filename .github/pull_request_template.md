# Pull Request

## Type

- [ ] GitHub Copilot primitive, authored locally
- [ ] External import or adapted external content
- [ ] Documentation
- [ ] Validation script or workflow
- [ ] Deliverable or rendered artifact

## External Import Checklist

Complete this section when the pull request imports or adapts content from `github/awesome-copilot` or another external source.

- [ ] Source repository and source URL are documented.
- [ ] License is compatible with this repository.
- [ ] Imported or adapted content includes provenance metadata where supported.
- [ ] No hardcoded secrets, tokens, or credentials are present.
- [ ] No unreviewed absolute paths or platform-specific assumptions remain.
- [ ] Script or workflow changes were reviewed for shell injection and unsafe permissions.
- [ ] The content follows repository copy rules.

## Validation

```bash
bash .github/scripts/audit-primitives.sh
bash .github/scripts/audit-skills.sh
bash .github/scripts/audit-external-content.sh
bash .github/scripts/validate-deliverables.sh
bash .github/scripts/generate-llms-txt.sh --check
```

Validation status:

- [ ] Passed locally
- [ ] Not run, reason documented below

## Notes

Add any critical findings, blockers, or follow-up work here.
