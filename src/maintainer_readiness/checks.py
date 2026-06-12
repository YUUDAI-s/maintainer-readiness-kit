from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import subprocess
from typing import Iterable


@dataclass(frozen=True)
class CheckSpec:
    check_id: str
    label: str
    weight: int
    candidates: tuple[str, ...]
    fix: str


CHECKS: tuple[CheckSpec, ...] = (
    CheckSpec("readme", "README explains purpose and usage", 12, ("README.md", "README.rst"), "Add a README with install, quick start, and limitations."),
    CheckSpec("license", "Open source license is present", 12, ("LICENSE", "LICENSE.md", "COPYING"), "Add a recognized open source license."),
    CheckSpec("contributing", "Contributor guide is present", 8, ("CONTRIBUTING.md", "docs/CONTRIBUTING.md"), "Add CONTRIBUTING.md with setup and contribution flow."),
    CheckSpec("security", "Security policy is present", 10, ("SECURITY.md", ".github/SECURITY.md"), "Add SECURITY.md with supported versions and disclosure contact."),
    CheckSpec("code_of_conduct", "Code of conduct is present", 5, ("CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"), "Add a code of conduct or link to the community standard."),
    CheckSpec("issue_template", "Issue template is present", 8, (".github/ISSUE_TEMPLATE",), "Add bug and feature issue templates."),
    CheckSpec("pr_template", "Pull request template is present", 8, (".github/PULL_REQUEST_TEMPLATE.md", "PULL_REQUEST_TEMPLATE.md"), "Add a pull request template with test and risk prompts."),
    CheckSpec("ci", "Continuous integration workflow is present", 10, (".github/workflows",), "Add a minimal CI workflow that runs tests or smoke checks."),
    CheckSpec("tests", "Tests are present", 10, ("tests", "test"), "Add a small test suite or smoke test directory."),
    CheckSpec("manifest", "Package or project manifest is present", 8, ("pyproject.toml", "package.json", "go.mod", "Cargo.toml", "pom.xml"), "Add a package manifest or project metadata file."),
    CheckSpec("docs", "Docs or examples are present", 5, ("docs", "examples"), "Add docs or examples for contributors and users."),
    CheckSpec("changelog", "Changelog or release notes are present", 4, ("CHANGELOG.md", "RELEASES.md", "docs/releases.md"), "Add a changelog or release notes file."),
)


HIGH_RISK_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "service-account.json",
    "id_rsa",
    "id_ed25519",
}


@dataclass(frozen=True)
class EcosystemRule:
    ecosystem: str
    evidence: tuple[str, ...]
    recommendations: tuple[str, ...]


ECOSYSTEM_RULES: tuple[EcosystemRule, ...] = (
    EcosystemRule(
        "python",
        ("pyproject.toml", "requirements.txt", "setup.py", "setup.cfg"),
        (
            "Run `python -m unittest discover -s tests` or the documented test command in CI.",
            "Keep packaging metadata in `pyproject.toml` and publish wheels from tagged releases.",
            "Use `src/` layout or clear package discovery to avoid importing local files accidentally.",
            "Document supported Python versions and minimum dependency policy.",
        ),
    ),
    EcosystemRule(
        "node",
        ("package.json", "pnpm-lock.yaml", "package-lock.json", "yarn.lock"),
        (
            "Expose `npm test` or an equivalent package script and run it in CI.",
            "Commit one lockfile for apps, or document why libraries avoid lockfiles.",
            "Document supported Node.js versions in README or package metadata.",
            "Run a package audit or dependency review before releases.",
        ),
    ),
    EcosystemRule(
        "rust",
        ("Cargo.toml", "Cargo.lock"),
        (
            "Run `cargo test` and `cargo clippy` in CI.",
            "Document supported Rust toolchain or MSRV.",
            "Commit `Cargo.lock` for binaries and document lockfile policy for libraries.",
            "Keep release notes aligned with crate version changes.",
        ),
    ),
    EcosystemRule(
        "go",
        ("go.mod", "go.sum"),
        (
            "Run `go test ./...` in CI.",
            "Keep `go.mod` and `go.sum` committed and tidy.",
            "Document supported Go version and module path.",
            "Use tagged releases for module consumers.",
        ),
    ),
    EcosystemRule(
        "java",
        ("pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle"),
        (
            "Run Maven or Gradle tests in CI.",
            "Document the supported Java version and build tool version.",
            "Keep dependency update and vulnerability review policy clear.",
            "Align release notes with package or artifact versions.",
        ),
    ),
)


@dataclass
class CheckResult:
    check_id: str
    label: str
    passed: bool
    weight: int
    evidence: str
    fix: str


def inspect_project(root: Path | str, root_label: str | None = None) -> dict:
    root_path = Path(root).resolve()
    check_results = [run_check(root_path, spec) for spec in CHECKS]
    score = sum(item.weight for item in check_results if item.passed)
    max_score = sum(item.weight for item in check_results)
    percent = round((score / max_score) * 100, 1) if max_score else 0.0
    return {
        "root": str(root_path),
        "display_root": root_label or str(root_path),
        "score": score,
        "max_score": max_score,
        "percent": percent,
        "level": classify_level(percent),
        "checks": [asdict(item) for item in check_results],
        "ecosystems": detect_ecosystems(root_path),
        "git": get_git_metrics(root_path),
        "secret_warnings": find_high_risk_files(root_path),
    }


def classify_level(percent: float) -> str:
    if percent >= 90:
        return "ready"
    if percent >= 70:
        return "nearly-ready"
    return "needs-work"


def run_check(root: Path, spec: CheckSpec) -> CheckResult:
    evidence = find_first_existing(root, spec.candidates)
    return CheckResult(
        check_id=spec.check_id,
        label=spec.label,
        passed=evidence is not None,
        weight=spec.weight,
        evidence=evidence or "missing",
        fix=spec.fix,
    )


def find_first_existing(root: Path, candidates: Iterable[str]) -> str | None:
    for candidate in candidates:
        path = root / candidate
        if path.exists():
            if path.is_dir():
                child_count = sum(1 for _ in path.iterdir())
                if child_count == 0:
                    continue
            return candidate
    return None


def detect_ecosystems(root: Path) -> list[dict]:
    detected: list[dict] = []
    for rule in ECOSYSTEM_RULES:
        evidence = [candidate for candidate in rule.evidence if (root / candidate).exists()]
        if evidence:
            detected.append(
                {
                    "ecosystem": rule.ecosystem,
                    "evidence": evidence,
                    "recommendations": list(rule.recommendations),
                }
            )
    if not detected:
        detected.append(
            {
                "ecosystem": "generic",
                "evidence": [],
                "recommendations": [
                    "Document the primary runtime, test command, and release process.",
                    "Add a CI smoke check that exercises the project entry point.",
                    "Include examples that show the smallest useful workflow.",
                ],
            }
        )
    return detected


def get_git_metrics(root: Path) -> dict:
    if not (root / ".git").exists():
        inside = _git(root, "rev-parse", "--is-inside-work-tree")
        if inside.returncode != 0 or inside.stdout.strip() != "true":
            return {"available": False, "reason": "not a git repository"}

    branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    last_commit = _git(root, "log", "-1", "--format=%cI")
    count_90 = _git(root, "rev-list", "--count", "--since=90.days.ago", "HEAD")
    dirty = _git(root, "status", "--short")
    return {
        "available": last_commit.returncode == 0,
        "branch": branch.stdout.strip() if branch.returncode == 0 else None,
        "last_commit": last_commit.stdout.strip() if last_commit.returncode == 0 else None,
        "commits_last_90_days": _parse_int(count_90.stdout.strip()) if count_90.returncode == 0 else None,
        "dirty_files": len([line for line in dirty.stdout.splitlines() if line.strip()]) if dirty.returncode == 0 else None,
    }


def find_high_risk_files(root: Path) -> list[dict]:
    warnings: list[dict] = []
    ignored = {".git", ".venv", "venv", "__pycache__", "dist", "build"}
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.is_file() and path.name in HIGH_RISK_NAMES:
            warnings.append(
                {
                    "path": str(path.relative_to(root)),
                    "reason": "high-risk local credential/config filename",
                }
            )
    return warnings


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _parse_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None
