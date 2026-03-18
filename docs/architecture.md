# Solo Founder Agents — Architecture & Design

> 시스템 아키텍처, 멀티세션 조율, 메모리 구조, 향후 로드맵을 정리한 기술 문서.

---

## 1. 시스템 개요

TypeScript + Node.js 기반 npm 패키지. 1인 창업자를 위한 24/7 AI 비서 시스템.

```bash
npm install -g solo-founder-agents
solo-agents init          # 워크스페이스 초기화
solo-agents bot           # 메신저 봇 실행
solo-agents schedule      # 자동 스케줄러
solo-agents update        # npm 최신 버전 확인 + 자동 업데이트
solo-agents doctor        # 환경 진단
solo-agents status        # 대시보드
solo-agents run-routine   # 수동 루틴 실행
```

---

## 2. 코드 구조

```
package.json                     → npm 패키지 (solo-founder-agents)
bin/solo-agents.ts               → CLI 진입점
src/
  cli/                           → CLI 명령 (init, bot, schedule, update, doctor, status, run-routine)
  bot/
    agent-router.ts              → 60+ 키워드 → 23 에이전트 라우팅
    claude-runner.ts             → Claude Code --print 서브프로세스 실행
    index.ts                     → 봇 메인 (어댑터 생성 → 핸들러 연결 → 시작)
  messenger/
    base.ts                      → MessengerAdapter / MessageContext 인터페이스
    discord-adapter.ts           → discord.js 기반
    slack-adapter.ts             → @slack/bolt Socket Mode 기반
    telegram-adapter.ts          → node-telegram-bot-api 기반
    index.ts                     → 팩토리 (createAdapter / createAdapters)
  scheduler/
    routines.ts                  → 5개 루틴 정의 (cron 표현식)
    memory.ts                    → JSON 블록 추출 → JSONL append (중복 방지)
    index.ts                     → node-cron 등록 + 전 플랫폼 동시 전송
  util/
    config.ts                    → .env 읽기/쓰기, products.json 관리
    paths.ts                     → 에셋/워크스페이스/repos 경로 해석
    logger.ts                    → chalk 기반 로거
assets/                          → npm에 번들, init 시 워크스페이스로 복사
  agents/{team}/{agent}/SKILL.md → 에이전트 정의 (23개)
  routines/*.md                  → 루틴 프롬프트
  templates/                     → PRD, 핸드오프, 상태 템플릿
  core/                          → 오너 프로필, 원칙, 스타일
```

---

## 3. 3-Layer 컨텍스트 격리

```
Layer 0: Universal (core/)
  OWNER.md, PRINCIPLES.md, VOICE.md
  → 모든 제품/프로젝트 세션에 공유

Layer 1: Product (~/repos/{slug}/)
  CLAUDE.md, product/brief.md, product/weekly-state.md
  memory/hypotheses.jsonl, experiments.jsonl, decisions.jsonl, signals.jsonl
  → 제품 단위 격리. 다른 제품 컨텍스트 차단.

Layer 2: Project (~/repos/{slug}/projects/{id}/)
  CLAUDE.md, brief.md, team.yaml, program.md
  → 프로젝트 단위 격리. 에이전트 활성 목록 제한.
```

---

## 4. 메신저 멀티 플랫폼

`MESSENGER` 환경변수로 설정. 콤마로 동시 운영 가능:

```
MESSENGER=discord          # Discord만
MESSENGER=slack            # Slack만
MESSENGER=discord,slack    # 동시 운영
```

어댑터 패턴으로 구현. 모든 플랫폼이 동일한 `CommandHandler` 인터페이스를 공유:
- **bot 모드**: 명령 채널 메시지 수신 → 에이전트 라우팅 → Claude Code 실행 → 응답
- **notifier 모드**: 스케줄러가 루틴 결과를 모든 연결 플랫폼에 전송

---

## 5. 에이전트 라우팅

`src/bot/agent-router.ts`의 `AGENT_ROUTES` 딕셔너리:
- 60+ 한국어/영어 키워드 → 23 에이전트 매핑
- 메시지에서 키워드 탐지 → 해당 에이전트의 SKILL.md 로드 → 프롬프트에 주입
- 매칭 없으면 일반 모드로 폴백

---

## 6. 자동 루틴 + 메모리

### 스케줄

| 시간 (KST) | 루틴 | 채널 | 메모리 타겟 |
|------------|------|------|-----------|
| 06:00 매일 | Morning Brief | #daily-brief | - |
| 12:00 매일 | Signal Scan | #signals | signals.jsonl |
| 16:00 매일 | Experiment Check | #experiments | experiments.jsonl |
| 22:00 매일 | Daily Log | #daily-brief | decisions.jsonl |
| 일 20:00 | Weekly Review | #weekly-review | decisions.jsonl |

### JSONL 메모리 스키마

| 파일 | 필드 | 용도 |
|------|------|------|
| `hypotheses.jsonl` | id, statement, risk, method, status, date | 가설 관리 |
| `experiments.jsonl` | id, hypothesis_id, method, result, signal_strength, date, next_action | 실험 기록 |
| `decisions.jsonl` | date, decision, alternatives, reasoning, emotion_weight | 의사결정 기록 |
| `signals.jsonl` | date, source, type, content, relevance, action | 외부 시그널 |

### 메모리 저장 흐름

```
루틴 실행 → Claude Code 결과
  → ```json 블록 자동 추출 → JSONL append (중복 방지, 날짜 자동 추가)
  → memory/routine-logs/{id}-{timestamp}.md (항상 저장)
  → 메신저 채널 전송 (모든 연결 플랫폼)
```

---

## 7. 멀티 세션 팀 조율

### 현재 한계

- 단일 세션 순차 실행 → 컨텍스트 윈도우 공유, 병렬 불가
- 에이전트 간 맥락 전달 프로토콜 미정의
- 수정 시 전체 재실행 필요

### 개선 아키텍처

```
┌──────────────────────────────────────────┐
│         Orchestrator 세션 (조율만)         │
└────────┬────────────┬────────────┬───────┘
         │            │            │
    ┌────▼────┐ ┌────▼─────┐ ┌───▼──────┐
    │Experience│ │ Strategy │ │  Growth   │
    │  세션    │ │  세션     │ │  세션     │
    └─────────┘ └──────────┘ └──────────┘
         │            │            │
         └────────────┼────────────┘
                      ▼
             projects/{id}/ (공유 파일시스템)
```

**원칙:**
1. Orchestrator는 조율만 (실행 X)
2. 각 팀은 독립 세션에서 실행
3. 파일 시스템이 세션 간 통신 채널
4. `_handoff.md`가 맥락 전달 표준

### 핸드오프 프로토콜

```markdown
# Handoff: [출발 에이전트] → [도착 에이전트]

## Summary — 핵심 발견 3줄 요약
## Artifacts — 생성된 산출물 목록
## Key Decisions — 결정 사항과 근거
## Context for Next Agent — 다음 에이전트가 알아야 할 맥락
## Open Questions — 미해결 질문
## Dependencies — 선행 조건
```

### 워크플로우 상태 추적 (`_status.yaml`)

```yaml
workflow:
  - stage: research
    agents: [user-researcher, desk-researcher]
    status: completed  # pending | in_progress | completed | needs_revision
    handoff: stage-1-research/_handoff.md
  - stage: planning
    agents: [feature-planner, scope-estimator]
    status: in_progress
    blocked_by: []
  - stage: design
    agents: [ux-designer, ui-designer]
    status: pending
    blocked_by: [planning]
```

### 병렬 실행 패턴 (PMF 탐색)

```
Phase 1 — 리서치 (병렬)
├── [Experience] User Researcher + Desk Researcher
└── [Strategy] Idea Refiner

Phase 2 — 기획 + 브랜딩 (병렬)
├── [Strategy] PMF Planner → Feature Planner
└── [Growth] Brand Marketer

Phase 3 — 디자인
└── [Experience] UX Designer → UI Designer

Phase 4 — 개발 + 마케팅 (병렬)
├── [Engineering] FDE or Frontend + Backend
└── [Growth] GTM Strategist + Content Writer

Phase 5 — 런칭
└── [Growth] Paid Marketer
```

직렬 8T → 병렬 5T (~37% 단축)

### 세션 시작

```bash
# Orchestrator (PRD 생성)
cd my-workspace && claude

# Experience Team (병렬)
claude --prompt "projects/{id}/sessions/experience/CLAUDE.md 읽고 작업 시작"

# Strategy Team (병렬)
claude --prompt "projects/{id}/sessions/strategy/CLAUDE.md 읽고 작업 시작"
```

---

## 8. 에이전트 → 팀 매핑

| Stage | 팀 | 에이전트 경로 |
|-------|-----|-------------|
| Research | Experience | `agents/experience/user-researcher/SKILL.md`, `desk-researcher/SKILL.md` |
| Branding | Growth | `agents/growth/brand-marketer/SKILL.md` |
| Planning | Strategy | `agents/strategy/pmf-planner/`, `feature-planner/`, `scope-estimator/` |
| Design | Experience | `agents/experience/ux-designer/`, `ui-designer/` |
| Development | Engineering | `agents/engineering/architect/`, `fde/`, `creative-frontend/`, `backend-developer/`, `api-developer/` |
| Marketing | Growth | `agents/growth/gtm-strategist/`, `content-writer/`, `paid-marketer/` |
| Analysis | Strategy | `agents/strategy/data-analyst/SKILL.md` |

---

## 9. 업데이트 전략 (OpenClaw 방식)

```bash
solo-agents update              # npm 최신 버전 확인 → 자동 업데이트
solo-agents update --channel dev  # 개발 채널
solo-agents doctor              # 환경 진단 (Node, Docker, Claude, 토큰, 설정)
```

- npm registry에서 최신 버전 조회 (`npm view solo-founder-agents version`)
- 로컬 `package.json` 버전과 비교
- 사용자 확인 후 `npm update -g solo-founder-agents` 실행

---

## 10. 향후 로드맵

### 단기
- [ ] `solo-agents orchestrate` CLI — 워크플로우 단계별 자동 팀 세션 실행
- [ ] `_status.yaml` 자동 업데이트 Hook
- [ ] 핸드오프 검증 체크리스트 자동화
- [ ] CI/CD 파이프라인 (테스트 + 린트)

### 중기
- [ ] 웹 대시보드 (status의 웹 버전)
- [ ] Claude Code 실행당 토큰/비용 로깅
- [ ] 일일 실행 한도 설정
- [ ] `solo-agents new-project` CLI 구현

### 장기 (MiroFish 참고)
- [ ] 데이터 분석/예측 모듈 (Python 백엔드)
- [ ] 지식 그래프 기반 시그널 분석
- [ ] 멀티에이전트 시뮬레이션 (시나리오 예측)

---

## 11. 레퍼런스

- [OpenClaw](https://github.com/openclaw/openclaw) — npm 패키지 배포 + update/doctor CLI 패턴
- [MiroFish](https://github.com/666ghj/MiroFish) — 멀티에이전트 시뮬레이션, 데이터 분석/예측 확장 방향
