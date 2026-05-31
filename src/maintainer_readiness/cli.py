from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .checks import inspect_project
from .github import fetch_github_repo
from .report import render_markdown
from .templates import write_templates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainer-readiness",
        description="Generate maintainer-readiness reports for OSS repositories.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a repository.")
    inspect_parser.add_argument("path", nargs="?", default=".", help="Repository path to inspect.")
    inspect_parser.add_argument("--repo", help="Optional GitHub repo as owner/name or URL.")
    inspect_parser.add_argument("--output", help="Write Markdown report to this path.")
    inspect_parser.add_argument("--root-label", help="Display label to use instead of the absolute local root path.")
    inspect_parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
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
    result = inspect_project(args.path, root_label=args.root_label)
    github = None
    if args.repo:
        github = fetch_github_repo(args.repo)
    exit_code = readiness_exit_code(result, args.fail_under)

    if args.json:
        payload = {"readiness": result, "github": github}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return exit_code

    markdown = render_markdown(result, github)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8", newline="\n")
        print(f"Wrote {output_path}")
    else:
        print(markdown)
    return exit_code


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
