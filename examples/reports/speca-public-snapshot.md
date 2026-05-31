# Maintainer Readiness Report

- Generated: 2026-05-31T07:33:14+00:00
- Root: `NyxFoundation/speca local checkout`
- Score: **73 / 100** (73.0%)
- Level: **nearly-ready**

## Public GitHub Signals

- Repository: [NyxFoundation/speca](https://github.com/NyxFoundation/speca)
- Visibility: `public`
- Stars: `422`
- Forks: `27`
- Open issues: `9`
- Last push: `2026-05-15T22:36:11Z`

## Local Maintenance Signals

- Branch: `main`
- Last commit: `2026-05-07T14:01:02+09:00`
- Commits in last 90 days: `318`
- Dirty files: `2`

## Passing Signals

- README explains purpose and usage: `README.md` (+12)
- Open source license is present: `LICENSE` (+12)
- Issue template is present: `.github/ISSUE_TEMPLATE` (+8)
- Pull request template is present: `.github/PULL_REQUEST_TEMPLATE.md` (+8)
- Continuous integration workflow is present: `.github/workflows` (+10)
- Tests are present: `tests` (+10)
- Package or project manifest is present: `pyproject.toml` (+8)
- Docs or examples are present: `docs` (+5)

## Missing Signals

- Contributor guide is present: Add CONTRIBUTING.md with setup and contribution flow. (+8)
- Security policy is present: Add SECURITY.md with supported versions and disclosure contact. (+10)
- Code of conduct is present: Add a code of conduct or link to the community standard. (+5)
- Changelog or release notes are present: Add a changelog or release notes file. (+4)

## Ecosystem Recommendations

### Python

- Evidence: `pyproject.toml`
- Run `python -m unittest discover -s tests` or the documented test command in CI.
- Keep packaging metadata in `pyproject.toml` and publish wheels from tagged releases.
- Use `src/` layout or clear package discovery to avoid importing local files accidentally.
- Document supported Python versions and minimum dependency policy.

## High-Risk File Warnings

- No high-risk credential filenames found.

## Maintainer Program Notes

- Use this report as evidence, not as a guarantee of eligibility.
- Do not claim usage, adoption, or maintainer permissions that cannot be verified.
- For new repositories, describe the project as early-stage and explain the concrete maintainer workflow it supports.
- Keep human approval in the loop for issue triage, PR review, releases, and public communication.
