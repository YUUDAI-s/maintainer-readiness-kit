# Maintainer Readiness Kit Instructions

- Keep the CLI dependency-light and usable with only the Python standard library.
- Do not add network calls to `inspect` unless the user explicitly passes
  `--repo`.
- `inspect` must never write to the target repository except for the requested
  report output path.
- `init` may create starter files, but it must not overwrite files unless
  `--force` is passed.
- Tests should run with `python -m unittest`.
