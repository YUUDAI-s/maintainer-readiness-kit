# Maintainer Readiness Kit

[![Maintainer readiness](https://github.com/YUUDAI-s/maintainer-readiness-kit/actions/workflows/maintainer-readiness.yml/badge.svg)](https://github.com/YUUDAI-s/maintainer-readiness-kit/actions/workflows/maintainer-readiness.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](pyproject.toml)

Maintainer Readiness Kit is a small, dependency-light CLI that audits an open
source repository for maintainer-facing signals: documentation, license files,
security policy, issue and pull request templates, CI, tests, recent git
activity, and high-risk local secret files.

The goal is simple: give solo and small-team maintainers a repeatable report
they can use before publishing a repository, onboarding contributors, or asking
for support from open source maintainer programs.

## What It Helps You Decide

Use it when you need a quick answer to:

- Is this repository ready to make public?
- What maintainer files are missing before I invite contributors?
- Will CI fail if the repository falls below a readiness threshold?
- What ecosystem-specific maintenance steps should I add next?
- Can I share a report without leaking my local machine path?

## Features

- Scores maintainer-readiness signals with evidence and suggested fixes.
- Reads local git activity without requiring network access.
- Optionally enriches the report with public GitHub repository signals.
- Generates starter maintainer templates for `CONTRIBUTING.md`,
  `SECURITY.md`, issue templates, pull request templates, and a GitHub Actions
  smoke workflow.
- Performs a conservative high-risk file check before public release.
- Outputs Markdown or JSON for CI and handoff docs.
- Classifies readiness as `ready`, `nearly-ready`, or `needs-work`.
- Detects Python, Node.js, Rust, and Go manifests and adds ecosystem-specific
  maintainer recommendations.

## Quick Start

Install from the repository:

```powershell
git clone https://github.com/YUUDAI-s/maintainer-readiness-kit.git
cd maintainer-readiness-kit
python -m pip install -e .
maintainer-readiness inspect . --output readiness-report.md
maintainer-readiness inspect . --fail-under 90
```

After the package is published to PyPI:

```powershell
python -m pip install maintainer-readiness-kit
maintainer-readiness inspect . --output readiness-report.md
```

For local source development without installation:

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect . --output readiness-report.md
python -m maintainer_readiness inspect . --fail-under 90
```

Typical output:

```text
Score: 100 / 100 (100.0%)
Level: ready
Ecosystem Recommendations: Python
High-Risk File Warnings: No high-risk credential filenames found.
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
python -m maintainer_readiness inspect . --root-label public-sample
```

The Markdown report includes:

- overall readiness score,
- readiness level,
- passing and missing signals,
- local git maintenance evidence,
- optional public GitHub evidence,
- high-risk file warnings,
- ecosystem-specific recommendations,
- next actions before public release.

For CI, use `--fail-under` to make the command return a non-zero exit code when
the readiness percentage is below your chosen threshold.

### GitHub Actions

```yaml
name: Maintainer readiness

on:
  pull_request:
  push:
    branches: [main]

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m pip install maintainer-readiness-kit
      - run: maintainer-readiness inspect . --fail-under 80
```

### `init`

```powershell
python -m maintainer_readiness init .
```

This writes starter maintainer files only when they do not already exist:

- `CONTRIBUTING.md`
- `SECURITY.md`
- `MAINTAINERS.md`
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

## Maintainer Workflows

This project is built for routine maintainer tasks:

- pre-publication checks before making a repository public,
- contributor onboarding checks before accepting outside PRs,
- release-readiness checks before tagging a version,
- safety checks before attaching reports to sponsorship or maintainer-support
  applications,
- CI-friendly JSON output for repeatable repository hygiene reviews.

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

See [ROADMAP.md](ROADMAP.md) for near-term maintainer-focused work.
See [examples/reports](examples/reports) for generated reports from real
repositories.
See [docs/pypi.md](docs/pypi.md) for package build and publishing notes.

## License

MIT
