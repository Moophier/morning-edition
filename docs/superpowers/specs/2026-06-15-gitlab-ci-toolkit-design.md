# GitLab CI Toolkit — Design Spec

## Overview

A CLI tool for GitLab CI/CD automation targeting both gitlab.com and self-hosted GitLab instances. Focuses on dev environment pipeline operations.

## Scope

**In scope:**
- Pipeline monitoring (watch, status, logs)
- Runner management (list, tag, pause/unpause)
- Artifact management (list, download, clean)
- Deployment to dev environment
- Pipeline report generation

**Out of scope:**
- Multi-environment promotion (staging, prod)
- Job triggering (manual pipeline runs)
- Project/group management
- Merge request interactions

## Architecture

### CLI Framework
- **Click** for command-line interface
- **python-gitlab** for GitLab API interactions

### Command Structure
```
gitlab-ci
├── pipeline
│   ├── watch     # Watch and display running pipeline status
│   ├── status    # Show current pipeline status
│   └── logs      # Stream pipeline job logs
├── runner
│   ├── list      # List available runners
│   └── manage    # Pause/unpause runners
├── artifact
│   ├── list      # List artifacts for a project
│   ├── clean     # Delete old artifacts
│   └── download  # Download artifacts
├── deploy
│   └── dev       # Deploy latest pipeline to dev
└── report
    └── summary    # Pipeline statistics and trends
```

### Configuration
- GitLab URL: `--url` flag or `GITLAB_URL` env var (default: gitlab.com)
- API Token: `--token` flag or `GITLAB_TOKEN` env var (required)
- Project: `--project` flag or `GITLAB_PROJECT` env var

### Authentication
Token-based authentication via:
- Personal Access Token (PAT)
- Project access token
- Group access token

Token passed via CLI flag or environment variable.

## Components

### GitLabClient
Wrapper around `python-gitlab` providing:
- Connection management (gitlab.com vs self-hosted)
- Project resolution
- Error handling with user-friendly messages

### PipelineWatcher
Monitors running pipelines with:
- Configurable refresh interval
- Status formatting (color-coded output)
- Job-level breakdown
- Failure notifications

### RunnerManager
Runner operations:
- Filter by tag
- Group by status (online/offline/paused)
- Bulk pause/unpause

### ArtifactManager
Artifact lifecycle:
- List with size and age
- Filter by job/ref
- Bulk deletion with confirmation

### Deployer
Dev deployment:
- Trigger deployment to dev environment
- Track deployment status
- Configurable namespace/project mapping

### Reporter
Pipeline analytics:
- Success/failure rates
- Average duration
- Trends over time (daily/weekly)

## Data Flow

```
User CLI Command
       ↓
   Click Handler
       ↓
  GitLabClient (python-gitlab)
       ↓
    GitLab API
       ↓
  Formatted Output
```

## Error Handling

- Network failures → retry with exponential backoff, then user-friendly error
- Auth failures → clear message about token validation
- Not found → specific resource type + identifier in error
- Permission denied → suggest required scope

## Output Format

- Human-readable by default (colorized terminal output)
- JSON output option via `--json` flag
- Quiet mode via `--quiet` flag (minimal output)

## Testing Strategy

- Unit tests for formatters and helpers
- Integration tests against a test GitLab instance (mocked)
- CLI smoke tests for each command

## File Structure

```
gitlab-ci-toolkit/
├── src/
│   └── gitlab_ci_toolkit/
│       ├── __init__.py
│       ├── cli.py           # Click CLI setup
│       ├── client.py        # GitLab client wrapper
│       ├── commands/
│       │   ├── pipeline.py
│       │   ├── runner.py
│       │   ├── artifact.py
│       │   ├── deploy.py
│       │   └── report.py
│       └── utils/
│           └── formatting.py
├── tests/
├── pyproject.toml
└── README.md
```