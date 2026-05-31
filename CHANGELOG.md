# Changelog

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
