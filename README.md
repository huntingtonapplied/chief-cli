<div align="center">
  <img src=".readme/logo.png" alt="Chief CLI" width="360"><br><br>
</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#license)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Install](https://img.shields.io/badge/install-curl%20%7C%20bash-3775a9.svg)](#installation)
[![Status](https://img.shields.io/badge/status-active-success.svg)](#)

-----------------

**Chief CLI** is the command-line client for [Chief](../README.md), the accessible smart card deployment platform. It lets you manage your Chief organizations, browse card applets, and check releases directly from your terminal — a thin client that talks to a running Chief API.

Use it to script and inspect the platform without the web wizard: list and fetch organizations, browse the applet catalog, view portfolio metrics, and check for new CLI releases. Ideal for CI pipelines, headless environments, and quick status checks.

## Installation

```bash
curl -fsSL https://downloads.badgechief.com/cli/install.sh | bash
```

From source (a clone of this repo):

```bash
pip install -e .
```

`chief-cli` is not published on PyPI; use the installer above or a source install.

Standalone binary:

```bash
./install.sh --version <version>
```

## Authentication

Authenticate interactively, then the CLI stores your credentials:

```bash
chief login
```

Config lives at `~/.chief/config.yaml`:

```yaml
api_key: your-api-key
api_url: http://localhost:8004
```

Or configure via environment variables:

- `CHIEF_API_KEY` — your Chief API key
- `CHIEF_API_URL` — API base URL (default `http://localhost:8004`)
- `CHIEF_DOWNLOADS_BASE_URL` — binary download host (default `https://downloads.badgechief.com`)
- `CHIEF_NO_UPDATE_CHECK=1` — disable update checks

## Commands

| Command | Description |
|---|---|
| `chief login` | Authenticate with Chief |
| `chief orgs list` | List organizations |
| `chief orgs get <id>` | Get organization details |
| `chief applets list` | List card applets |
| `chief applets get <id>` | Get applet details |
| `chief releases latest` | Get the latest release |
| `chief releases check-update` | Check for CLI updates |
| `chief metrics portfolio` | View portfolio metrics |
| `chief status` | Show system status |
| `chief doctor` | Diagnose connection issues |
| `chief completion bash` | Generate shell completion |

## Example

```bash
chief login                       # authenticate
chief orgs list                   # list your organizations
chief applets list                # browse the applet catalog
chief orgs list --output json     # machine-readable output
chief orgs list --quiet           # IDs only
chief status                      # system status
```

## Talks to

The Chief API (default `http://localhost:8004`) — see the [backend README](../backend/README.md). Standalone binaries are served from `https://downloads.badgechief.com`.

## Documentation & resources

- Root: [Chief README](../README.md) · Backend: [backend/README.md](../backend/README.md)

## License

This project is licensed under the MIT License.
