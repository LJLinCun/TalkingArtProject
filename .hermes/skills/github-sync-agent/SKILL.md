---
name: github-sync-agent
description: "GitHub sync workflow for AI-Agent prompt engineering repos"
version: 1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Sync, CI-CD, Prompt-Engineering]
    related_skills: [github-auth, github-pr-workflow, github-repo-management]
---

# GitHub Sync Workflow for AI-Agent Projects

This skill encapsulates the complete sync flow for talkingart-project style repos — optimized for AI-agent prompt engineering frameworks (OpenClaw, Hermes).

## Pre-requisites
- Git installed and configured with user identity
- Personal Access Token or SSH key for authentication
- Working directory containing the repo

## Core Workflow

### 1. Detect Authentication Method

```bash
detect_auth_method() {
  if command -v gh &>/dev/null && gh auth status &>/dev/null; then
    echo "AUTH_METHOD=gh"
elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
  export GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    echo "AUTH_METHOD=curl"
else
  echo "Need to configure authentication first"
fi
}
```

### 2. Configure Remote URL (Token-based)

```bash
# Store token in git credential cache — no plaintext storage
git config --global credential.helper cache --timeout=28800

# Set remote with embedded token for immediate auth
git remote set-url origin https://ghp_[TOKEN]@github.com/LJLinCun/TalkingArtProject.git
```

### 3. Commit & Push Sequence

```bash
# Stage all changes
git add -A

# Create commit with conventional prefix for agent projects
git commit -m "chore: sync prompt engineering framework updates [schema_v1]"

# Force push with tracking setup — safe for CI/CD pipelines
git push -u origin main 2>/dev/null || git push -u origin master
```

### 4. Verify Push Success

```bash
# Confirm remote branch exists
git ls-remote --heads origin | grep -E "(main|master)"

# Check for recent commits on remote
git log --oneline -3 --all --graph
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | Personal Access Token (alternative to credential helper) |
| `SCHEMA_VERSION` | Prompt framework version — defaults to v1.0 |

## Integration Points

- **Hermes Agent**: Call via `skill_view(name='github-sync-agent')`
- **OpenClaw AI System**: Use as part of agent deployment pipeline
- **CI/CD Scripts**: Embed in GitHub Actions workflow YAML files

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| `fatal: could not read Password` | Token not available — configure via credential helper or set GITHUB_TOKEN env var |
| `Authentication failed` | Check token scopes: must include `repo`, `workflow`, and `read:org` if applicable |
| `Permission denied` | Verify repo name in remote URL matches actual GitHub repository |
| Branch mismatch | Run `git fetch --all && git branch -r` to sync local tracking branches |
