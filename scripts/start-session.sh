#!/bin/bash
# 팀 세션 시작 스크립트
# Usage: ./scripts/start-session.sh <project_id> <team>
# Example: ./scripts/start-session.sh jeonse-guard experience

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

PROJECT_ID="${1:?Usage: $0 <project_id> <team>}"
TEAM="${2:?Usage: $0 <project_id> <team>. team: orchestrator|strategy|experience|growth|engineering}"

PROJECT_DIR="$ROOT_DIR/projects/$PROJECT_ID"
SESSION_DIR="$PROJECT_DIR/sessions/$TEAM"

# Validate
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project '$PROJECT_ID' not found at $PROJECT_DIR"
    exit 1
fi

if [ ! -f "$SESSION_DIR/CLAUDE.md" ]; then
    echo "Error: Session context not found at $SESSION_DIR/CLAUDE.md"
    exit 1
fi

echo "Starting $TEAM session for project: $PROJECT_ID"
echo ""

# Show current workflow status
if [ -f "$PROJECT_DIR/_status.yaml" ]; then
    echo "=== Workflow Status ==="
    grep -A2 "status:" "$PROJECT_DIR/_status.yaml" | head -30
    echo ""
fi

# Show pending handoffs for this team
echo "=== Pending Handoffs ==="
for handoff in "$PROJECT_DIR"/stage-*/_handoff.md; do
    if [ -f "$handoff" ]; then
        stage_dir=$(dirname "$handoff")
        stage_name=$(basename "$stage_dir")
        echo "  - $stage_name: $(head -1 "$handoff")"
    fi
done
echo ""

# Launch Claude Code session
echo "Launching Claude Code session..."
cd "$ROOT_DIR"
claude "projects/$PROJECT_ID/sessions/$TEAM/CLAUDE.md 읽고 작업 시작"
