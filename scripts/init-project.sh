#!/bin/bash
# 프로젝트 초기화 스크립트
# Usage: ./scripts/init-project.sh <project_id> <project_name> <type>
# Example: ./scripts/init-project.sh jeonse-guard "전세사기 예방 서비스" pmf

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

PROJECT_ID="${1:?Usage: $0 <project_id> <project_name> <type>}"
PROJECT_NAME="${2:?Usage: $0 <project_id> <project_name> <type>}"
PROJECT_TYPE="${3:?Usage: $0 <project_id> <project_name> <type>. type: pmf|experiment|feature|rebrand|prototype}"
TODAY=$(date +%Y-%m-%d)

PROJECT_DIR="$ROOT_DIR/projects/$PROJECT_ID"

if [ -d "$PROJECT_DIR" ]; then
    echo "Error: Project '$PROJECT_ID' already exists at $PROJECT_DIR"
    exit 1
fi

echo "Initializing project: $PROJECT_NAME ($PROJECT_ID)"
echo "Type: $PROJECT_TYPE"
echo ""

# Create directory structure
mkdir -p "$PROJECT_DIR/sessions"

# Generate _status.yaml from template
sed \
    -e "s/{{project_id}}/$PROJECT_ID/g" \
    -e "s/{{project_name}}/$PROJECT_NAME/g" \
    -e "s/{{pmf | experiment | feature | rebrand | prototype}}/$PROJECT_TYPE/g" \
    -e "s/{{YYYY-MM-DD}}/$TODAY/g" \
    "$ROOT_DIR/templates/status.yaml" > "$PROJECT_DIR/_status.yaml"

# Generate session CLAUDE.md files for each team
for team in orchestrator strategy experience growth engineering; do
    mkdir -p "$PROJECT_DIR/sessions/$team"

    # Copy from template and replace placeholders
    if [ -f "$ROOT_DIR/templates/session-$team.md" ]; then
        sed \
            -e "s|{{project_id}}|$PROJECT_ID|g" \
            -e "s|{{project_root}}|$ROOT_DIR|g" \
            "$ROOT_DIR/templates/session-$team.md" > "$PROJECT_DIR/sessions/$team/CLAUDE.md"
    fi
done

# Create empty changelog
cat > "$PROJECT_DIR/_changelog.md" << 'CHANGELOG'
# Changelog

## v1 ($(date +%Y-%m-%d))
- 프로젝트 초기화
CHANGELOG

# Fix the date in changelog
sed -i '' "s/\$(date +%Y-%m-%d)/$TODAY/" "$PROJECT_DIR/_changelog.md"

echo "Project initialized at: $PROJECT_DIR"
echo ""
echo "Directory structure:"
find "$PROJECT_DIR" -type f | sort | sed "s|$ROOT_DIR/||"
echo ""
echo "Next steps:"
echo "  1. PRD를 작성하세요: $PROJECT_DIR/prd.md"
echo "  2. Orchestrator 세션에서 워크플로우를 시작하세요"
echo "  3. 팀 세션은 다음 명령으로 시작:"
echo "     claude \"projects/$PROJECT_ID/sessions/<team>/CLAUDE.md 읽고 작업 시작\""
