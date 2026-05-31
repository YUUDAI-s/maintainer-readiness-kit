# Usage Guide

## Inspect a Local Repository

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect C:\path\to\repo --output readiness-report.md
```

The command reads files, directories, and local git metadata. It does not write
to the inspected repository unless you choose an output path inside that
repository.

## Add Public GitHub Signals

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect . --repo owner/name --output readiness-report.md
```

This calls the public GitHub repository API and adds stars, forks, open issues,
visibility, and last-push information to the report.

## Initialize Starter Maintainer Files

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness init C:\path\to\repo
```

The command skips existing files by default. Use `--force` only when you intend
to overwrite starter maintainer files.

## Suggested Release Flow

1. Run `inspect` locally and fix missing high-value signals.
2. Run tests or a project-specific smoke check.
3. Confirm that no high-risk credential files are present.
4. Publish the repository.
5. Run `inspect --repo owner/name` after publication and attach the generated
   report to the release or maintainer handoff notes.
