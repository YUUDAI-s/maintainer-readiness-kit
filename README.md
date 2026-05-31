# Maintainer Readiness Kit

Maintainer Readiness Kit is a small, dependency-light CLI that audits an open
source repository for maintainer-facing signals: documentation, license files,
security policy, issue and pull request templates, CI, tests, recent git
activity, and high-risk local secret files.

The goal is simple: give solo and small-team maintainers a repeatable report
they can use before publishing a repository, onboarding contributors, or asking
for support from open source maintainer programs.

## Features

- Scores maintainer-readiness signals with evidence and suggested fixes.
- Reads local git activity without requiring network access.
- Optionally enriches the report with public GitHub repository signals.
- Generates starter maintainer templates for `CONTRIBUTING.md`,
  `SECURITY.md`, issue templates, pull request templates, and a GitHub Actions
  smoke workflow.
- Performs a conservative high-risk file check before public release.
- Outputs Markdown or JSON for CI and handoff docs.

## Quick Start

```powershell
cd maintainer-readiness-kit
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
python -m maintainer_readiness inspect . --output readiness-report.md
```

To include public GitHub signals:

```powershell
python -m maintainer_readiness inspect . --repo YUUDAI-s/maintainer-readiness-kit --output readiness-report.md
```

To add starter maintainer files to another repository:

```powershell
python -m maintainer_readiness init C:\path\to\repo
```

Use `--force` only when you intentionally want to overwrite an existing starter
file.

## Commands

### `inspect`

```powershell
python -m maintainer_readiness inspect . --output readiness-report.md
python -m maintainer_readiness inspect . --json
python -m maintainer_readiness inspect . --repo owner/name
```

The Markdown report includes:

- overall readiness score,
- passing and missing signals,
- local git maintenance evidence,
- optional public GitHub evidence,
- high-risk file warnings,
- next actions before public release.

### `init`

```powershell
python -m maintainer_readiness init .
```

This writes starter maintainer files only when they do not already exist:

- `CONTRIBUTING.md`
- `SECURITY.md`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/maintainer-readiness.yml`

## Design Principles

- Honest evidence over vanity metrics.
- Minimal runtime dependencies.
- Useful defaults for maintainers who work alone.
- No external writes from `inspect`.
- No claims that a repository qualifies for any external program.

## Limitations

This tool cannot prove that a repository is widely adopted, safe, or eligible
for any benefit. It only turns common maintainer signals into a compact,
verifiable report. Program applications still require accurate information
about the applicant, repository, role, usage, and maintainer status.

## Development

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
python -m maintainer_readiness inspect . --output readiness-report.md
```

## License

MIT
