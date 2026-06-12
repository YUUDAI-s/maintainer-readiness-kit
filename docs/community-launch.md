# Community Launch Notes

Use this document when sharing Maintainer Readiness Kit with developer
communities. Keep the positioning accurate: this is an early-stage maintainer
tool, not a popularity or eligibility guarantee.

## Good Targets

- GitHub Discussions in this repository.
- Hacker News `Show HN` if the project has a clear demo and the maintainer can
  respond to feedback.
- Reddit communities such as `r/opensource` or `r/github` only after reading
  their posting rules.
- Language-specific maintainer communities when the post includes a concrete
  Python, Node.js, Rust, or Go example.

Avoid drive-by posting. The goal is feedback from maintainers, not low-quality
traffic.

## Short Announcement

Maintainer Readiness Kit is a dependency-light CLI that generates a shareable
readiness report for open source repositories. It checks maintainer basics like
README, license, contributing guide, security policy, issue/PR templates, CI,
tests, release notes, git activity, stale public issues/PRs, ecosystem-specific
recommendations, and high-risk local credential filenames.

I built it for solo and small-team maintainers who want a concrete checklist
before publishing a repository, onboarding contributors, or preparing evidence
for maintainer-support programs.

Repo: https://github.com/YUUDAI-s/maintainer-readiness-kit
GitHub Action: `YUUDAI-s/maintainer-readiness-kit@v0.6.0`
Public demo: https://github.com/YUUDAI-s/maintainer-readiness-kit-action-demo

## Show HN Draft

Title:

```text
Show HN: Maintainer Readiness Kit - a CLI checklist for OSS maintainers
```

Body:

```text
I built Maintainer Readiness Kit, a small Python CLI that generates a
shareable maintainer-readiness report for open source repositories.

It checks README, license, contributing docs, security policy, issue/PR
templates, CI, tests, release notes, local git activity, public GitHub signals,
stale issues/PRs, ecosystem-specific recommendations, and high-risk credential
filenames such as .env.local.

The intended use case is a solo or small-team maintainer asking: "Is this repo
ready to publish or invite contributors to?"

I would like feedback from maintainers on which readiness signals are useful,
which weights are wrong, and what the tool should detect next.

Repo: https://github.com/YUUDAI-s/maintainer-readiness-kit
GitHub Action: `YUUDAI-s/maintainer-readiness-kit@v0.6.0`
Public demo: https://github.com/YUUDAI-s/maintainer-readiness-kit-action-demo
```

## Feedback Questions

- Which readiness signal should carry more or less weight?
- Should stale issue/PR thresholds be configurable?
- Which ecosystem should be added after Python, Node.js, Rust, and Go?
- Would SARIF, Markdown, or JSON be the most useful CI output for your workflow?

## Posting Rules

- Do not claim broad adoption until it exists.
- Do not imply that a readiness score proves eligibility for any external
  program.
- Include a direct repo link and one concrete example report.
- Stay available to answer comments for at least 24 hours after posting.
