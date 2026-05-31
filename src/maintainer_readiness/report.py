from __future__ import annotations

from datetime import datetime, timezone


def render_markdown(result: dict, github: dict | None = None) -> str:
    lines: list[str] = []
    lines.append("# Maintainer Readiness Report")
    lines.append("")
    lines.append(f"- Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append(f"- Root: `{result['root']}`")
    lines.append(f"- Score: **{result['score']} / {result['max_score']}** ({result['percent']}%)")
    lines.append(f"- Level: **{result['level']}**")
    lines.append("")

    if github:
        lines.append("## Public GitHub Signals")
        lines.append("")
        lines.append(f"- Repository: [{github.get('full_name')}]({github.get('html_url')})")
        lines.append(f"- Visibility: `{github.get('visibility')}`")
        lines.append(f"- Stars: `{github.get('stars')}`")
        lines.append(f"- Forks: `{github.get('forks')}`")
        lines.append(f"- Open issues: `{github.get('open_issues')}`")
        lines.append(f"- Last push: `{github.get('pushed_at')}`")
        lines.append("")

    git = result.get("git", {})
    lines.append("## Local Maintenance Signals")
    lines.append("")
    if git.get("available"):
        lines.append(f"- Branch: `{git.get('branch')}`")
        lines.append(f"- Last commit: `{git.get('last_commit')}`")
        lines.append(f"- Commits in last 90 days: `{git.get('commits_last_90_days')}`")
        lines.append(f"- Dirty files: `{git.get('dirty_files')}`")
    else:
        lines.append(f"- Git metadata unavailable: {git.get('reason', 'unknown')}")
    lines.append("")

    passed = [item for item in result["checks"] if item["passed"]]
    missing = [item for item in result["checks"] if not item["passed"]]
    lines.append("## Passing Signals")
    lines.append("")
    for item in passed:
        lines.append(f"- {item['label']}: `{item['evidence']}` (+{item['weight']})")
    if not passed:
        lines.append("- None yet.")
    lines.append("")

    lines.append("## Missing Signals")
    lines.append("")
    for item in missing:
        lines.append(f"- {item['label']}: {item['fix']} (+{item['weight']})")
    if not missing:
        lines.append("- None.")
    lines.append("")

    warnings = result.get("secret_warnings", [])
    lines.append("## High-Risk File Warnings")
    lines.append("")
    if warnings:
        for warning in warnings:
            lines.append(f"- `{warning['path']}`: {warning['reason']}")
    else:
        lines.append("- No high-risk credential filenames found.")
    lines.append("")

    lines.append("## Maintainer Program Notes")
    lines.append("")
    lines.append("- Use this report as evidence, not as a guarantee of eligibility.")
    lines.append("- Do not claim usage, adoption, or maintainer permissions that cannot be verified.")
    lines.append("- For new repositories, describe the project as early-stage and explain the concrete maintainer workflow it supports.")
    lines.append("- Keep human approval in the loop for issue triage, PR review, releases, and public communication.")
    lines.append("")
    return "\n".join(lines)
