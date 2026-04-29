#!/usr/bin/env bash
#
# TaskTorrent contributor bootstrap one-liner.
#
# Usage:
#   curl -sSL https://romeo111.github.io/task_torrent/install.sh | bash
#
# What it does:
#   1. Verifies dependencies (git, gh, python 3.10+).
#   2. Authenticates via gh if needed.
#   3. Lists registered TaskTorrent consumers (projects).
#   4. You pick one or auto-select the next available chunk.
#   5. Hands off to the consumer's bootstrap_contributor.sh.
#
# This script does NOT clone, claim, or modify anything on its own.
# It's a multi-project shim that delegates to the consumer's own scripts.
#
# Verify before piping to bash:
#   curl -sSL https://romeo111.github.io/task_torrent/install.sh > install.sh
#   sha256sum -c <(curl -sSL https://romeo111.github.io/task_torrent/install.sh.sha256)

set -euo pipefail

CONSUMERS_URL="https://romeo111.github.io/task_torrent/metrics.json"

cat <<'BANNER'
   _____         _   _____                          _
  |_   _|_ _ ___| | _|_   _|__  _ __ _ __ ___ _ __ | |_
    | |/ _` / __| |/ / | |/ _ \| '__| '__/ _ \ '_ \| __|
    | | (_| \__ \   <  | | (_) | |  | | |  __/ | | | |_
    |_|\__,_|___/_|\_\ |_|\___/|_|  |_|  \___|_| |_|\__|

  Distributed AI-assisted contribution work.
  https://romeo111.github.io/task_torrent/

BANNER

# --- 1. Deps ---

for cmd in git curl jq; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERROR: '$cmd' is required but not on PATH." >&2
    echo "Install: git from https://git-scm.com/, jq from https://jqlang.github.io/jq/" >&2
    exit 1
  fi
done
if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: GitHub CLI 'gh' is required. Install: https://cli.github.com/" >&2
  exit 1
fi

# --- 2. gh auth ---

if ! gh auth status >/dev/null 2>&1; then
  echo "→ Not authenticated with GitHub. Run: gh auth login"
  echo "  Then re-run this script."
  exit 2
fi
echo "✓ gh authenticated"

# --- 3. List consumers ---

echo
echo "Fetching available projects..."
metrics_json=$(curl -fsSL "$CONSUMERS_URL")
if [[ -z "$metrics_json" ]]; then
  echo "ERROR: could not fetch consumer registry from $CONSUMERS_URL" >&2
  exit 3
fi

mapfile -t consumer_names < <(printf '%s' "$metrics_json" | jq -r '.per_consumer[].name')
if [[ ${#consumer_names[@]} -eq 0 ]]; then
  echo "No active projects on TaskTorrent right now."
  exit 0
fi

echo
echo "Active TaskTorrent projects:"
printf '%s' "$metrics_json" | jq -r \
  '.per_consumer[] | "  [\(.name)] \(.display_name) — \(.chunks_claimable) claimable chunks"'

# --- 4. Pick one ---

echo
echo "Pick a project by name (or press Enter for the one with most claimable chunks):"
read -r choice
if [[ -z "$choice" ]]; then
  choice=$(printf '%s' "$metrics_json" | jq -r \
    'first(.per_consumer | sort_by(.chunks_claimable) | reverse | .[]).name')
  echo "→ auto-picked: $choice"
fi

# --- 5. Hand off to consumer's bootstrap ---

repo=$(printf '%s' "$metrics_json" | jq -r ".per_consumer[] | select(.name == \"$choice\") | .repo")
if [[ -z "$repo" || "$repo" == "null" ]]; then
  echo "ERROR: project '$choice' not registered." >&2
  exit 4
fi

echo
echo "Project: $choice → github.com/$repo"
echo "Cloning + bootstrapping..."
echo
clone_dir="./$choice"
if [[ ! -d "$clone_dir/.git" ]]; then
  gh repo clone "$repo" "$clone_dir"
fi
cd "$clone_dir"

if [[ ! -x scripts/tasktorrent/bootstrap_contributor.sh ]]; then
  echo "ERROR: $repo does not ship scripts/tasktorrent/bootstrap_contributor.sh" >&2
  echo "       (Consumer must adopt the TaskTorrent reference scripts. See" >&2
  echo "        https://github.com/romeo111/task_torrent/blob/main/docs/cross-repo-contract.md)" >&2
  exit 5
fi

bash scripts/tasktorrent/bootstrap_contributor.sh --no-clone --repo "$repo"
