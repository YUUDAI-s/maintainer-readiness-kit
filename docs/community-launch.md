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
Release: https://github.com/YUUDAI-s/maintainer-readiness-kit/releases/tag/v0.6.1
GitHub Action: `YUUDAI-s/maintainer-readiness-kit@v0.6.0`
Public demo: https://github.com/YUUDAI-s/maintainer-readiness-kit-action-demo
PyPI: pending Trusted Publisher setup

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
Release: https://github.com/YUUDAI-s/maintainer-readiness-kit/releases/tag/v0.6.1
GitHub Action: `YUUDAI-s/maintainer-readiness-kit@v0.6.0`
Public demo: https://github.com/YUUDAI-s/maintainer-readiness-kit-action-demo
PyPI: pending Trusted Publisher setup
```

## Reddit Draft

Target communities should be chosen only after reading their current rules.
`r/opensource` and `r/github` may be relevant, but self-promotion rules vary.

Title:

```text
Feedback wanted: a CLI readiness checklist for small OSS maintainers
```

Body:

```text
I maintain an early-stage OSS tool called Maintainer Readiness Kit. It is a
small Python CLI and GitHub Action that generates a maintainer-readiness report
for a repository.

It checks README, license, contributing/security docs, issue and PR templates,
CI, tests, release notes, git activity, stale public issues/PRs,
ecosystem-specific recommendations, SARIF output, and high-risk local
credential filenames.

I am looking for practical maintainer feedback, not asking for stars. The main
question is: which signals are actually useful before publishing a repo or
inviting contributors, and which checks are noise?

Repo: https://github.com/YUUDAI-s/maintainer-readiness-kit
Public GitHub Action demo: https://github.com/YUUDAI-s/maintainer-readiness-kit-action-demo
Latest release: https://github.com/YUUDAI-s/maintainer-readiness-kit/releases/tag/v0.6.1

PyPI install is not live yet; the GitHub release has wheel/sdist assets, and
PyPI Trusted Publisher setup is the remaining packaging step.
```

## X Draft

Use this only from an account that can respond to replies. Do not automate
repeated reposts or replies.

```text
I'm building Maintainer Readiness Kit, a small OSS CLI/GitHub Action that checks whether a repo is ready for contributors: README, license, security docs, CI, tests, stale issues/PRs, SARIF, and maintainer workflow signals.

Feedback from OSS maintainers wanted:
https://github.com/YUUDAI-s/maintainer-readiness-kit
```

## Manual Posting Checklist

1. Confirm the account is logged in.
2. Read the target community rules on the same day.
3. Use the repository URL as the primary link.
4. Keep claims accurate: early-stage, public demo available, PyPI pending.
5. Do not ask for stars, upvotes, comments, or artificial engagement.
6. Stay available to answer feedback for 24 hours.
7. Record the posted URL in this document or in a follow-up issue.

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
