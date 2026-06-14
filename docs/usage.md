# Usage Guide

## Inspect a Local Repository

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect C:\path\to\repo --output readiness-report.md
```

The command reads files, directories, and local git metadata. It does not write
to the inspected repository unless you choose an output path inside that
repository.

Use `--root-label` when you want to publish or share a report without exposing a
local absolute path:

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect C:\path\to\repo --root-label my-project --output report.md
```

## Add Public GitHub Signals

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect . --repo owner/name --output readiness-report.md
```

This calls the public GitHub repository API and adds stars, forks, open issues,
visibility, last-push information, and a sampled stale issue/PR summary to the
report.

The stale summary reads up to 100 open GitHub issue records sorted by oldest
update time. GitHub represents pull requests in the issues API, so the report
splits sampled items into issues and PRs before counting items that have not
been updated in 30 days.

Use `--stale-days` to change that threshold:

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect . --repo owner/name --stale-days 14 --output readiness-report.md
```

## Reuse Defaults From a Config File

Create `maintainer-readiness.toml` or `.maintainer-readiness.toml` in the
repository root:

```toml
repo = "owner/name"
output = "readiness-report.md"
sarif = "readiness.sarif"
badge-json = "readiness-badge.json"
root-label = "public-demo"
stale-days = 14
fail-under = 90
```

Then run:

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect C:\path\to\repo
```

Use `--config path\to\maintainer-readiness.toml` to choose a specific file.
CLI flags override config values.

The repository also includes a copy-ready example at
`examples/maintainer-readiness.toml`.

## Fail CI Below a Threshold

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect . --fail-under 90
```

The command still prints the report, but exits with code `1` when the readiness
percentage is below the threshold. This is useful for pull request and release
checks.

## Write SARIF for Code Scanning

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect . --sarif readiness.sarif
```

SARIF output includes failed maintainer checks, high-risk credential filename
warnings, and stale public GitHub issue/PR notes when `--repo` is used.

## Write Badge JSON

```powershell
$env:PYTHONPATH = "src"
python -m maintainer_readiness inspect . --badge-json readiness-badge.json
```

The badge file follows the Shields endpoint schema and can be published from a
docs site, release artifact, or static dashboard.

## Use the GitHub Action

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: YUUDAI-s/maintainer-readiness-kit@v0.7.0
    with:
      repo: owner/name
      fail-under: "80"
      stale-days: "30"
      output: readiness-report.md
      sarif: readiness.sarif
      badge-json: readiness-badge.json
      config: maintainer-readiness.toml
```

The action installs the CLI from the checked-out action version and runs the
same `inspect` command that is available locally. Action inputs are passed as
CLI flags, so explicit inputs override matching values from
`maintainer-readiness.toml`. Leave an Action input empty when you want the
config file to provide that value.

## Ecosystem Recommendations

The report detects common manifests and adds maintainer recommendations for:

- Python: `pyproject.toml`, `requirements.txt`, `setup.py`, `setup.cfg`
- Node.js: `package.json`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`
- Rust: `Cargo.toml`, `Cargo.lock`
- Go: `go.mod`, `go.sum`
- Java/JVM: `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle`

If no known manifest is detected, the report falls back to generic maintainer
recommendations.

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

## Public Sample Reports

Generated reports are kept in `examples/reports/`. When adding reports from
local checkouts, use `--root-label` and avoid publishing reports for private
client or business repositories.
