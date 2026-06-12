# Roadmap

## 0.2.0

- [x] Add language-specific recommendations for Python, Node.js, Rust, and Go.
- [x] Add a `--fail-under` option for CI gates.
- [x] Add a report section for stale issues and stale pull requests when
  `--repo` is provided.
- Add a release-readiness checklist that compares changelog, tags, and local
  version metadata.

## 0.3.0

- Add maintainer workload summaries for issue triage and PR review.
- [x] Add configurable stale issue and pull request thresholds.
- [x] Add SARIF output for CI and code-scanning workflows.
- [x] Add Java and JVM ecosystem recommendations.
- Add JSON schema output for downstream automations.
- Add a docs site generated from the CLI help and report examples.

## Open Maintainer Questions

- Which maintainer signals should be weighted differently for very small
  projects?
- Which safety checks can be added without collecting private repository data?
- How should reports represent early-stage projects honestly without punishing
  new maintainers for low adoption?
