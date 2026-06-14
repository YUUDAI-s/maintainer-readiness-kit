from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .checks import inspect_project
from .badge import render_badge
from .config import load_inspect_config
from .github import fetch_github_repo
from .report import render_markdown
from .sarif import render_sarif
from .templates import write_templates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainer-readiness",
        description="Generate maintainer-readiness reports for OSS repositories.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a repository.")
    inspect_parser.add_argument("path", nargs="?", default=".", help="Repository path to inspect.")
    inspect_parser.add_argument(
        "--config",
        help=(
            "Config file path. Defaults to maintainer-readiness.toml or "
            ".maintainer-readiness.toml in the inspected root."
        ),
    )
    inspect_parser.add_argument("--repo", help="Optional GitHub repo as owner/name or URL.")
    inspect_parser.add_argument("--output", help="Write Markdown report to this path.")
    inspect_parser.add_argument("--sarif", help="Write SARIF report to this path.")
    inspect_parser.add_argument("--badge-json", help="Write Shields endpoint JSON to this path.")
    inspect_parser.add_argument("--root-label", help="Display label to use instead of the absolute local root path.")
    inspect_parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    inspect_parser.add_argument(
        "--stale-days",
        type=int,
        default=None,
        metavar="DAYS",
        help="Treat open GitHub issues and pull requests as stale after DAYS without updates.",
    )
    inspect_parser.add_argument(
        "--fail-under",
        type=float,
        metavar="SCORE",
        help="Exit non-zero when the readiness percentage is below SCORE.",
    )

    init_parser = subparsers.add_parser("init", help="Write starter maintainer templates.")
    init_parser.add_argument("path", nargs="?", default=".", help="Repository path to initialize.")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing starter files.")
    init_parser.add_argument("--json", action="store_true", help="Print JSON output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "inspect":
        return run_inspect(args)
    if args.command == "init":
        return run_init(args)
    parser.error("unknown command")
    return 2


def run_inspect(args: argparse.Namespace) -> int:
    config = load_inspect_config(args.path, args.config)
    stale_days = coerce_int(option_value(args.stale_days, config.values, "stale_days", 30), "--stale-days")
    fail_under = coerce_optional_float(option_value(args.fail_under, config.values, "fail_under", None), "--fail-under")
    root_label = option_value(args.root_label, config.values, "root_label", None)
    repo = option_value(args.repo, config.values, "repo", None)
    output = option_path(args.output, config, "output")
    sarif = option_path(args.sarif, config, "sarif")
    badge_json = option_path(args.badge_json, config, "badge_json")
    json_output = args.json or bool(config.values.get("json", False))

    if stale_days <= 0:
        raise SystemExit("--stale-days must be a positive integer")
    result = inspect_project(args.path, root_label=root_label)
    github = None
    if repo:
        github = fetch_github_repo(repo, stale_days=stale_days)
    exit_code = readiness_exit_code(result, fail_under)
    if sarif:
        sarif_path = Path(sarif)
        sarif_path.parent.mkdir(parents=True, exist_ok=True)
        sarif_path.write_text(json.dumps(render_sarif(result, github), ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    if badge_json:
        badge_path = Path(badge_json)
        badge_path.parent.mkdir(parents=True, exist_ok=True)
        badge_path.write_text(json.dumps(render_badge(result), ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    if json_output:
        payload = {"readiness": result, "github": github}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return exit_code

    markdown = render_markdown(result, github)
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8", newline="\n")
        print(f"Wrote {output_path}")
    else:
        print(markdown)
    return exit_code


def option_value(cli_value, config: dict, key: str, default):
    if cli_value is not None:
        return cli_value
    return config.get(key, default)


def option_path(cli_value: str | None, config, key: str):
    if cli_value is not None:
        return cli_value
    value = config.values.get(key)
    if value is None:
        return None
    path = Path(str(value))
    if path.is_absolute() or config.base_dir is None:
        return str(path)
    return str(config.base_dir / path)


def coerce_int(value, label: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise SystemExit(f"{label} must be an integer") from exc


def coerce_optional_float(value, label: str) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise SystemExit(f"{label} must be a number") from exc


def readiness_exit_code(result: dict, fail_under: float | None) -> int:
    if fail_under is None:
        return 0
    if fail_under < 0 or fail_under > 100:
        raise SystemExit("--fail-under must be between 0 and 100")
    return 1 if result["percent"] < fail_under else 0


def run_init(args: argparse.Namespace) -> int:
    result = write_templates(args.path, force=args.force)
    if args.json:
        print(json.dumps({"templates": result}, ensure_ascii=False, indent=2))
    else:
        for item in result:
            print(f"{item['status']}: {item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
