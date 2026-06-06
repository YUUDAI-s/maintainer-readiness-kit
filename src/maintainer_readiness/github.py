from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def fetch_github_repo(repo: str, token: str | None = None) -> dict:
    normalized = repo.strip().removeprefix("https://github.com/").strip("/")
    if normalized.count("/") != 1:
        raise ValueError("repo must be owner/name or https://github.com/owner/name")

    auth_token = token or os.environ.get("GITHUB_TOKEN")
    payload = _github_get_json(f"https://api.github.com/repos/{normalized}", auth_token, normalized)
    try:
        open_items = _github_get_json(
            f"https://api.github.com/repos/{normalized}/issues?state=open&per_page=100&sort=updated&direction=asc",
            auth_token,
            normalized,
        )
        workload = summarize_open_items(open_items)
    except RuntimeError as exc:
        workload = {"activity_error": str(exc)}

    return {
        "full_name": payload.get("full_name"),
        "html_url": payload.get("html_url"),
        "description": payload.get("description"),
        "visibility": payload.get("visibility"),
        "stars": payload.get("stargazers_count"),
        "forks": payload.get("forks_count"),
        "open_issues": payload.get("open_issues_count"),
        "created_at": payload.get("created_at"),
        "updated_at": payload.get("updated_at"),
        "pushed_at": payload.get("pushed_at"),
        "default_branch": payload.get("default_branch"),
        **workload,
    }


def _github_get_json(url: str, auth_token: str | None, repo_label: str) -> dict | list[dict]:
    request = Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    if auth_token:
        request.add_header("Authorization", f"Bearer {auth_token}")

    try:
        with urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"GitHub API returned HTTP {exc.code} for {repo_label}") from exc
    except URLError as exc:
        raise RuntimeError(f"GitHub API request failed for {repo_label}: {exc.reason}") from exc


def summarize_open_items(items: list[dict], now: datetime | None = None, stale_days: int = 30) -> dict:
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=stale_days)
    issues = []
    pulls = []
    for item in items:
        updated_at = _parse_github_datetime(item.get("updated_at"))
        if updated_at is None:
            continue
        if item.get("pull_request"):
            pulls.append(updated_at)
        else:
            issues.append(updated_at)

    return {
        "activity_sample_limit": 100,
        "stale_days": stale_days,
        "open_issue_items_sampled": len(issues),
        "open_pr_items_sampled": len(pulls),
        "stale_issue_items": sum(updated_at < cutoff for updated_at in issues),
        "stale_pr_items": sum(updated_at < cutoff for updated_at in pulls),
        "oldest_open_issue_updated_at": _oldest_iso(issues),
        "oldest_open_pr_updated_at": _oldest_iso(pulls),
    }


def _parse_github_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _oldest_iso(values: list[datetime]) -> str | None:
    if not values:
        return None
    return min(values).isoformat(timespec="seconds").replace("+00:00", "Z")
