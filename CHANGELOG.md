# Changelog

All notable changes to the Chief CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Pre-1.0 policy:** Minor versions (0.x) may include breaking changes.

## [0.1.0] - Unreleased

### Added
- Initial release with `login`, `orgs`, `applets`, `releases`, `metrics`, `status`, `doctor`, and `completion` commands
- `--output/-o` flag for `table`, `json`, or `yaml` output formats
- `--no-color` flag (also honors the `NO_COLOR` env var) for plain output
- `--verbose/-v` flag for INFO-level logging to stderr
- `--debug` flag for DEBUG-level logging (HTTP requests)
- `--ci` flag for CI/CD pipeline usage (no color, no spinners, no prompts); auto-detected from `CI`, `GITHUB_ACTIONS`, `GITLAB_CI` env vars
- `chief doctor` command — checks Python, config, API connectivity, auth, and shell completion
- Retry logic with exponential backoff for transient HTTP errors (429, 500, 502, 503, 504) and network failures; configurable via `CHIEF_MAX_RETRIES` env var
- Distinct exit codes: 2 (auth), 3 (not found), 4 (validation), 5 (network), 6 (server), 7 (duplicate), 130 (SIGINT), 143 (SIGTERM)
- Config validation with typo detection (`did you mean 'api_key'?`) on startup
- Configurable request timeout via `CHIEF_TIMEOUT` env var or `timeout` config key
- SIGTERM signal handling across all commands (clean exit with code 143)
- Top-level KeyboardInterrupt handler as a safety net for all commands
- Non-blocking version update check (background thread, 24h throttle, disabled in CI; disable with `CHIEF_NO_UPDATE_CHECK=1`)
- Shell completion for bash, zsh, and fish
- Rich terminal output with table, JSON, and YAML formats
- Nuitka standalone binary builds published via SEGA to `https://downloads.badgechief.com`

### Configuration
- API key via `CHIEF_API_KEY` env var or config file
- API base URL via `CHIEF_API_URL` env var (default port 8002)
