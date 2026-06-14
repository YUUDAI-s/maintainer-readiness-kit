# Maintainer Readiness Kit

[![Maintainer readiness](https://github.com/YUUDAI-s/maintainer-readiness-kit/actions/workflows/maintainer-readiness.yml/badge.svg)](https://github.com/YUUDAI-s/maintainer-readiness-kit/actions/workflows/maintainer-readiness.yml)
[![GitHub Action](https://img.shields.io/badge/GitHub%20Action-ready-brightgreen.svg)](action.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](pyproject.toml)

Maintainer Readiness Kit is a small, dependency-light CLI that audits an open
source repository for maintainer-facing signals: documentation, license files,
security policy, issue and pull request templates, CI, tests, recent git
activity, and high-risk local secret files.

The goal is simple: give solo and small-team maintainers a repeatable report
they can use before publishing a repository, onboarding contributors, or asking
for support from open source maintainer programs.

## Who Should Use It

- Maintainers preparing a repository for public contributors.
- Solo developers who need a concrete pre-release checklist.
- Teams that want CI to fail when maintainer basics regress.
- Open source applicants who need honest, shareable evidence instead of vague
  claims.

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
- Summarizes stale open issues and pull requests for public GitHub reports.
- Generates starter maintainer templates for `CONTRIBUTING.md`,
  `SECURITY.md`, issue templates, pull request templates, and a GitHub Actions
  smoke workflow.
- Performs a conservative high-risk file check before public release.
- Outputs Markdown or JSON for CI and handoff docs.
- Outputs SARIF for CI and code-scanning workflows.
- Outputs Shields endpoint badge JSON for project dashboards.
- Runs as a reusable GitHub Action.
- Reads `maintainer-readiness.toml` / `.maintainer-readiness.toml` defaults.
- Classifies readiness as `ready`, `nearly-ready`, or `needs-work`.
- Detects Python, Node.js, Rust, Go, and Java/JVM manifests and adds
  ecosystem-specific maintainer recommendations.

## Quick Start

Install from the repository:

```powershell
git clone https://github.com/YUUDAI-s/maintainer-readiness-kit.git
cd maintainer-readiness-kit
python -m pip install -e .
maintainer-readiness inspect . --output readiness-report.md
maintainer-readiness inspect . --fail-under 90
```

Use it directly in GitHub Actions:

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: YUUDAI-s/maintainer-readiness-kit@v0.7.0
    with:
      repo: owner/name
      fail-under: "80"
      output: readiness-report.md
      sarif: readiness.sarif
      badge-json: readiness-badge.json
```

Public demo repository:
[`YUUDAI-s/maintainer-readiness-kit-action-demo`](https://github.com/YUUDAI-s/maintainer-readiness-kit-action-demo)
uses the reusable action in CI.

Install from PyPI:

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
python -m maintainer_readiness inspect . --repo owner/name --stale-days 14
python -m maintainer_readiness inspect . --sarif readiness.sarif
python -m maintainer_readiness inspect . --badge-json readiness-badge.json
python -m maintainer_readiness inspect . --config maintainer-readiness.toml
```

Config files use simple TOML scalar values:

```toml
repo = "owner/name"
output = "readiness-report.md"
sarif = "readiness.sarif"
badge-json = "readiness-badge.json"
root-label = "public-demo"
stale-days = 14
fail-under = 90
```

`inspect` automatically reads `maintainer-readiness.toml` or
`.maintainer-readiness.toml` from the inspected root when present. CLI flags
override config values.

See [examples/maintainer-readiness.toml](examples/maintainer-readiness.toml)
for a copy-ready configuration file.

The Markdown report includes:

- overall readiness score,
- readiness level,
- passing and missing signals,
- local git maintenance evidence,
- optional public GitHub evidence,
- stale open issue and pull request counts when `--repo` is used,
- high-risk file warnings,
- ecosystem-specific recommendations,
- next actions before public release.

For CI, use `--fail-under` to make the command return a non-zero exit code when
the readiness percentage is below your chosen threshold.

Use `--stale-days` with `--repo` when your project has a shorter or longer
triage window than the default 30 days.

Use `--sarif readiness.sarif` when you want failed checks and high-risk file
warnings in a code-scanning compatible format.

Use `--badge-json readiness-badge.json` when you want a Shields-compatible
endpoint JSON payload for a dashboard or docs site.

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
      - uses: YUUDAI-s/maintainer-readiness-kit@v0.7.0
        with:
          config: maintainer-readiness.toml
          repo: owner/name
          fail-under: "80"
          output: readiness-report.md
          sarif: readiness.sarif
          badge-json: readiness-badge.json
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: readiness.sarif
```

Action inputs are passed as CLI flags, so explicit inputs override matching
values from `maintainer-readiness.toml`. Leave an Action input empty when you
want the config file to provide that value.

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
See the public action demo at
[YUUDAI-s/maintainer-readiness-kit-action-demo](https://github.com/YUUDAI-s/maintainer-readiness-kit-action-demo).
See [docs/pypi.md](docs/pypi.md) for package build and publishing notes.
See [docs/community-launch.md](docs/community-launch.md) for community launch
copy and posting rules.
See [examples/github-action.yml](examples/github-action.yml) for a copyable
GitHub Actions workflow.

## License

MIT
