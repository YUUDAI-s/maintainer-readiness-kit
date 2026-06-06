from __future__ import annotations

from datetime import datetime, timezone


def render_markdown(result: dict, github: dict | None = None) -> str:
    lines: list[str] = []
    lines.append("# Maintainer Readiness Report")
    lines.append("")
    lines.append(f"- Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append(f"- Root: `{result.get('display_root', result['root'])}`")
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
        if github.get("activity_error"):
            lines.append(f"- Open issue/PR activity: unavailable ({github.get('activity_error')})")
        elif github.get("stale_days") is not None:
            lines.append(
                f"- Open issues sampled: `{github.get('open_issue_items_sampled')}` "
                f"(`{github.get('stale_issue_items')}` stale over {github.get('stale_days')} days)"
            )
            lines.append(
                f"- Open PRs sampled: `{github.get('open_pr_items_sampled')}` "
                f"(`{github.get('stale_pr_items')}` stale over {github.get('stale_days')} days)"
            )
            if github.get("oldest_open_issue_updated_at"):
                lines.append(f"- Oldest open issue update: `{github.get('oldest_open_issue_updated_at')}`")
            if github.get("oldest_open_pr_updated_at"):
                lines.append(f"- Oldest open PR update: `{github.get('oldest_open_pr_updated_at')}`")
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

    lines.append("## Ecosystem Recommendations")
    lines.append("")
    for item in result.get("ecosystems", []):
        evidence = ", ".join(f"`{value}`" for value in item.get("evidence", [])) or "no manifest detected"
        lines.append(f"### {item['ecosystem'].title()}")
        lines.append("")
        lines.append(f"- Evidence: {evidence}")
        for recommendation in item.get("recommendations", []):
            lines.append(f"- {recommendation}")
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
