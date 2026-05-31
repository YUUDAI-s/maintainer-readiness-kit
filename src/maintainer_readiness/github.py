from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def fetch_github_repo(repo: str, token: str | None = None) -> dict:
    normalized = repo.strip().removeprefix("https://github.com/").strip("/")
    if normalized.count("/") != 1:
        raise ValueError("repo must be owner/name or https://github.com/owner/name")

    request = Request(f"https://api.github.com/repos/{normalized}")
    request.add_header("Accept", "application/vnd.github+json")
    auth_token = token or os.environ.get("GITHUB_TOKEN")
    if auth_token:
        request.add_header("Authorization", f"Bearer {auth_token}")

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"GitHub API returned HTTP {exc.code} for {normalized}") from exc
    except URLError as exc:
        raise RuntimeError(f"GitHub API request failed for {normalized}: {exc.reason}") from exc

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
    }
