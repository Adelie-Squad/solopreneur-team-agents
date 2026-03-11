# solopreneur-agents 개선 계획

## 개선 목표
기존 SKILL.md 기반 에이전트 시스템에 24/7 자동화 인프라를 추가하여
Discord 봇 + 스케줄러 + CLI 도구로 완전한 솔로프리너 비서 시스템 구축.

## 구현 완료 항목

### 1. Discord Bot (`src/bot.py`)
- `#owner-command` 채널에서 명령 수신
- Claude Code `--print` 모드로 실행 후 응답
- 서버별 제품 자동 매핑
- 채널 자동 생성

### 2. Scheduler (`src/scheduler.py`)
- APScheduler 기반 24시간 루틴 실행
- 5개 루틴: Morning Brief, Signal Scan, Experiment Check, Daily Log, Weekly Review
- 제품별 병렬 실행
- Discord 채널 자동 보고 + 웹훅/파일 폴백

### 3. CLI Tools
- `cli/new_project.py`: 인터랙티브 프로젝트 생성
- `cli/status.py`: 전체 현황 대시보드

### 4. Setup Wizard (`setup.py`)
- 환경 확인 → .env 설정 → 제품 등록 → Docker 빌드 → Bot 초대 → 시작

### 5. Core Templates
- `core/OWNER.md`: 오너 프로필
- `core/PRINCIPLES.md`: 의사결정 원칙 (검증 우선, YODA 데이터 등)
- `core/VOICE.md`: 글쓰기 스타일 가이드

### 6. Routine Prompts (`routines/`)
- `morning-brief.md`: 오늘의 브리핑
- `signal-scan.md`: 시그널 탐지
- `experiment-check.md`: 실험 점검
- `daily-log.md`: 일일 기록
- `weekly-review.md`: 주간 회고

### 7. Docker 배포
- `Dockerfile`: Python 3.12 + Claude Code CLI
- `docker-compose.yml`: bot + scheduler 서비스

### 8. 3-Layer 컨텍스트 아키텍처
- Layer 0: Universal (core/) → 모든 세션 공유
- Layer 1: Product (~/repos/{slug}/) → 제품별 격리
- Layer 2: Project (projects/{id}/) → 프로젝트별 격리

### 9. JSONL 기반 메모리 시스템
- hypotheses.jsonl, experiments.jsonl, decisions.jsonl, signals.jsonl
- 스키마 헤더 + append 방식

## 참고
- plan_files/: 원본 설계 참고 파일
