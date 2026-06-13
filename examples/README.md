# Examples

This directory contains generated sample reports.

- `github-action.yml`: copyable GitHub Actions workflow that runs
  `YUUDAI-s/maintainer-readiness-kit@v0.6.1`.
- Public demo repo:
  `https://github.com/YUUDAI-s/maintainer-readiness-kit-action-demo`
- `reports/maintainer-readiness-kit.md`: report generated from this project.
- `reports/speca-public-snapshot.md`: report generated from a local checkout of
  the public `NyxFoundation/speca` repository. This project is not affiliated
  with SPECA; it is included as a public-repository sample.
- `reports/local-node-app-sanitized.md`: sanitized report generated from a
  private local Node.js application to show how the tool handles non-public
  workspaces without exposing absolute paths or secrets.

Reports use `--root-label` so they can be shared without exposing local absolute
paths.
