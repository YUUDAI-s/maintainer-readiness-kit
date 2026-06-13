# PyPI Publishing

The package name is `maintainer-readiness-kit`.

## Install

```powershell
python -m pip install maintainer-readiness-kit
maintainer-readiness --version
```

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

## Trusted Publisher Values

The first manual publish attempts built and validated the package, then failed
at the trusted-publishing exchange because PyPI did not have a matching
publisher configured. After the pending publisher below was configured, the
manual publish workflow succeeded and created the PyPI project.

Configure these values in PyPI Trusted Publishing:

- PyPI project name: `maintainer-readiness-kit`
- Owner: `YUUDAI-s`
- Repository: `maintainer-readiness-kit`
- Workflow: `publish-python.yml`
- Environment: `pypi`

The GitHub OIDC subject observed from the failed publish attempt was:

```text
repo:YUUDAI-s/maintainer-readiness-kit:environment:pypi
```

Published package:

- PyPI: `https://pypi.org/project/maintainer-readiness-kit/`
- Version: `0.6.1`
- Successful workflow:
  `https://github.com/YUUDAI-s/maintainer-readiness-kit/actions/runs/27454249674`
