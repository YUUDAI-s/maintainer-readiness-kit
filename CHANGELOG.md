# Changelog

## 0.5.0 - 2026-06-12

- Added configurable stale issue and pull request thresholds with `--stale-days`.
- Added SARIF output for CI and code-scanning workflows with `--sarif`.
- Added Java/JVM ecosystem recommendations.

## 0.4.0 - 2026-06-06

- Added stale open issue and pull request summaries for public GitHub reports.
- Added community launch notes and a GitHub Discussion idea template.

## 0.3.2 - 2026-05-31

- Added a sanitized local Node application sample report.

## 0.3.1 - 2026-05-31

- Added PyPI packaging guidance and a manual publish workflow.
- Added public sample reports and clearer README usage examples.

## 0.3.0 - 2026-05-31

- Added ecosystem-specific recommendations for Python, Node.js, Rust, and Go.
- Added `inspect --root-label` for shareable reports that do not expose local paths.

## 0.2.0 - 2026-05-31

- Added `inspect --fail-under SCORE` for CI readiness gates.
- Updated the GitHub Actions workflow to enforce a minimum readiness score.
- Added CLI tests for fail-under behavior.

## 0.1.0 - 2026-05-31

- Added the initial `inspect` command for local maintainer-readiness reports.
- Added optional GitHub public repository signal enrichment.
- Added `init` command for starter maintainer templates.
- Added high-risk local credential filename warnings.
- Added readiness levels for clearer release and publication decisions.
- Added CI smoke workflow and sample report.
- Added maintainer responsibilities and review policy.
- Added unit tests for checks and template behavior.
