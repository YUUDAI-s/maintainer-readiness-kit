from __future__ import annotations

from pathlib import Path


TEMPLATES: dict[str, str] = {
    "CONTRIBUTING.md": """# Contributing

Thanks for helping improve this project.

## Local Setup

1. Fork and clone the repository.
2. Install the documented runtime.
3. Run the smoke test or unit tests before opening a pull request.

## Pull Requests

- Keep changes focused.
- Include tests or a manual verification note.
- Document behavior changes in the README or changelog when relevant.
""",
    "SECURITY.md": """# Security Policy

## Supported Versions

The default branch receives security fixes.

## Reporting a Vulnerability

Please open a private security advisory or contact the maintainer through the
repository owner profile. Do not disclose exploitable details publicly before a
fix or mitigation is available.
""",
    ".github/ISSUE_TEMPLATE/bug_report.yml": """name: Bug report
description: Report a reproducible bug.
title: "[Bug]: "
labels: ["bug"]
body:
  - type: textarea
    id: summary
    attributes:
      label: Summary
      description: What happened?
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Reproduction steps
      description: List the smallest steps that reproduce the issue.
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, version, runtime, and any relevant config.
""",
    ".github/ISSUE_TEMPLATE/feature_request.yml": """name: Feature request
description: Suggest an improvement.
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem would this solve?
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: Proposal
      description: Describe the smallest useful change.
""",
    ".github/PULL_REQUEST_TEMPLATE.md": """## Summary

## Verification

- [ ] Tests or smoke checks were run.
- [ ] Documentation was updated, or no docs change is needed.
- [ ] Security/privacy impact was considered.

## Notes for Maintainers
""",
    ".github/workflows/maintainer-readiness.yml": """name: Maintainer readiness

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
      - run: python -m unittest
""",
}


def write_templates(root: Path | str, force: bool = False) -> list[dict]:
    root_path = Path(root).resolve()
    written: list[dict] = []
    for relative_path, content in TEMPLATES.items():
        target = root_path / relative_path
        if target.exists() and not force:
            written.append({"path": relative_path, "status": "skipped"})
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        written.append({"path": relative_path, "status": "written"})
    return written
