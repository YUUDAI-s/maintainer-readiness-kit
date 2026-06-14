from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_CONFIG_NAMES = ("maintainer-readiness.toml", ".maintainer-readiness.toml")
KEY_ALIASES = {
    "badge-json": "badge_json",
    "badge_json": "badge_json",
    "fail-under": "fail_under",
    "fail_under": "fail_under",
    "json": "json",
    "output": "output",
    "repo": "repo",
    "root-label": "root_label",
    "root_label": "root_label",
    "sarif": "sarif",
    "stale-days": "stale_days",
    "stale_days": "stale_days",
}


@dataclass(frozen=True)
class InspectConfig:
    values: dict
    path: Path | None

    @property
    def base_dir(self) -> Path | None:
        return self.path.parent if self.path else None


def load_inspect_config(root: str | Path, config_path: str | None = None) -> InspectConfig:
    path = find_config_path(root, config_path)
    if path is None:
        return InspectConfig({}, None)
    values = parse_simple_toml(path)
    return InspectConfig(values, path)


def find_config_path(root: str | Path, config_path: str | None = None) -> Path | None:
    if config_path:
        explicit = Path(config_path)
        if not explicit.exists():
            raise SystemExit(f"Config file not found: {explicit}")
        return explicit
    root_path = Path(root)
    if root_path.is_file():
        root_path = root_path.parent
    for name in DEFAULT_CONFIG_NAMES:
        candidate = root_path / name
        if candidate.exists():
            return candidate
    return None


def parse_simple_toml(path: Path) -> dict:
    values = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = strip_inline_comment(raw_line).strip()
        if not line:
            continue
        if line.startswith("["):
            raise SystemExit(f"{path}:{line_number}: TOML sections are not supported")
        if "=" not in line:
            raise SystemExit(f"{path}:{line_number}: expected KEY = VALUE")
        raw_key, raw_value = line.split("=", 1)
        key = normalize_key(raw_key.strip(), path, line_number)
        values[key] = parse_scalar(raw_value.strip(), path, line_number)
    return values


def normalize_key(raw_key: str, path: Path, line_number: int) -> str:
    key = raw_key.strip().strip('"').strip("'")
    normalized = KEY_ALIASES.get(key)
    if normalized is None:
        allowed = ", ".join(sorted(KEY_ALIASES))
        raise SystemExit(f"{path}:{line_number}: unsupported config key {key!r}; allowed keys: {allowed}")
    return normalized


def parse_scalar(raw_value: str, path: Path, line_number: int):
    if not raw_value:
        raise SystemExit(f"{path}:{line_number}: missing value")
    if raw_value[0] in {'"', "'"}:
        return parse_quoted_string(raw_value, path, line_number)
    lowered = raw_value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        if any(ch in raw_value for ch in (".", "e", "E")):
            return float(raw_value)
        return int(raw_value)
    except ValueError as exc:
        raise SystemExit(f"{path}:{line_number}: unsupported scalar value {raw_value!r}") from exc


def parse_quoted_string(raw_value: str, path: Path, line_number: int) -> str:
    quote = raw_value[0]
    if len(raw_value) < 2 or not raw_value.endswith(quote):
        raise SystemExit(f"{path}:{line_number}: unterminated string")
    return raw_value[1:-1]


def strip_inline_comment(line: str) -> str:
    quote = None
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
            continue
        if char == "#":
            return line[:index]
    return line
