# Chief CLI

CLI tool for Chief application management — manage organizations, applets, and releases from your terminal.

## Installation

```bash
pip install chief-cli
```

Or from source:
```bash
cd /Users/latarencebutts/ahl/chief/cli
pip install -e .
```

### Install Standalone Binary

```bash
./install.sh --version <version>
```

Environment:
- `CHIEF_DOWNLOADS_BASE_URL` (default: `https://downloads.badgechief.com`)

Disable update checks:
- `CHIEF_NO_UPDATE_CHECK=1`

## Quick Start

```bash
# Authenticate
chief login

# List organizations
chief orgs list

# List applets
chief applets list

# Check for updates
chief releases latest

# System status
chief status
```

## Commands

| Command | Description |
|---------|-------------|
| `chief login` | Authenticate with Chief |
| `chief orgs list` | List organizations |
| `chief orgs get <id>` | Get organization details |
| `chief applets list` | List applets |
| `chief applets get <id>` | Get applet details |
| `chief releases latest` | Get latest release |
| `chief releases check-update` | Check for updates |
| `chief metrics portfolio` | View portfolio metrics |
| `chief status` | Show system status |
| `chief doctor` | Diagnose connection issues |
| `chief completion bash` | Generate shell completion |

## Configuration

Config stored at `~/.chief/config.yaml`:
```yaml
api_key: your-api-key
api_url: http://localhost:8004
```

Or use environment variables:
- `CHIEF_API_KEY`
- `CHIEF_API_URL`

## Output Formats

```bash
chief orgs list --output json    # JSON output
chief orgs list --quiet          # IDs only
```
