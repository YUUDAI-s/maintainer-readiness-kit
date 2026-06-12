from __future__ import annotations


def render_badge(result: dict) -> dict:
    percent = float(result.get("percent", 0.0))
    if percent >= 90:
        color = "brightgreen"
    elif percent >= 70:
        color = "yellow"
    else:
        color = "red"
    return {
        "schemaVersion": 1,
        "label": "maintainer readiness",
        "message": f"{percent:.1f}%",
        "color": color,
    }
