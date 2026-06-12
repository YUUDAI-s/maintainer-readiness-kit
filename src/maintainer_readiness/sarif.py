from __future__ import annotations

from datetime import datetime, timezone


def render_sarif(result: dict, github: dict | None = None) -> dict:
    rules = []
    sarif_results = []
    for item in result.get("checks", []):
        rule_id = f"maintainer-readiness.{item['check_id']}"
        rules.append(
            {
                "id": rule_id,
                "name": item["label"],
                "shortDescription": {"text": item["label"]},
                "help": {"text": item["fix"]},
                "properties": {"weight": item["weight"]},
            }
        )
        if not item.get("passed"):
            sarif_results.append(
                {
                    "ruleId": rule_id,
                    "level": "warning",
                    "message": {"text": item["fix"]},
                    "locations": [_location(result, item.get("evidence") or ".")],
                }
            )

    rules.append(
        {
            "id": "maintainer-readiness.high-risk-file",
            "name": "High-risk credential filename",
            "shortDescription": {"text": "High-risk credential filename"},
            "help": {"text": "Remove local credential/config files before publishing the repository."},
        }
    )
    for warning in result.get("secret_warnings", []):
        sarif_results.append(
            {
                "ruleId": "maintainer-readiness.high-risk-file",
                "level": "error",
                "message": {"text": warning["reason"]},
                "locations": [_location(result, warning["path"])],
            }
        )

    if github and github.get("stale_issue_items"):
        rules.append(_github_rule("stale-issues", "Stale open issues"))
        sarif_results.append(_github_result("stale-issues", f"{github['stale_issue_items']} open issues are stale."))
    if github and github.get("stale_pr_items"):
        rules.append(_github_rule("stale-prs", "Stale open pull requests"))
        sarif_results.append(_github_result("stale-prs", f"{github['stale_pr_items']} open pull requests are stale."))

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Maintainer Readiness Kit",
                        "informationUri": "https://github.com/YUUDAI-s/maintainer-readiness-kit",
                        "rules": rules,
                    }
                },
                "invocations": [
                    {
                        "executionSuccessful": True,
                        "endTimeUtc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
                    }
                ],
                "results": sarif_results,
            }
        ],
    }


def _location(result: dict, path: str) -> dict:
    display_root = result.get("display_root") or result.get("root") or "."
    artifact = "." if path == "missing" else path
    return {
        "physicalLocation": {
            "artifactLocation": {
                "uri": artifact,
                "uriBaseId": display_root,
            }
        }
    }


def _github_rule(suffix: str, name: str) -> dict:
    return {
        "id": f"maintainer-readiness.github.{suffix}",
        "name": name,
        "shortDescription": {"text": name},
        "help": {"text": "Review stale public GitHub work as part of routine maintainer triage."},
    }


def _github_result(suffix: str, message: str) -> dict:
    return {
        "ruleId": f"maintainer-readiness.github.{suffix}",
        "level": "note",
        "message": {"text": message},
    }
