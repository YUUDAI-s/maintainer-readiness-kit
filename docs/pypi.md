# PyPI Publishing

The package name is `maintainer-readiness-kit`.

## Build Locally

```powershell
python -m pip install build twine
python -m build
python -m twine check dist/*
```

## Manual Publish

Publishing requires a PyPI account and API token.

```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-..."
python -m twine upload dist/*
```

Do not commit tokens, `.pypirc`, or terminal logs containing tokens.

## GitHub Trusted Publishing

The included `.github/workflows/publish-python.yml` workflow is manual-only.
Before running it:

1. Create the PyPI project or configure the pending project name.
2. Add this repository as a trusted publisher on PyPI.
3. Confirm the package version in `pyproject.toml`.
4. Run the workflow from GitHub Actions.

The workflow builds the package, runs `twine check`, and publishes with PyPI
trusted publishing.
