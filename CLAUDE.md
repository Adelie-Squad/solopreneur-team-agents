# Solo Founder Agents

> 1인 창업자를 위한 AI 에이전트 협업 시스템. 팀 기반 멀티 세션 구조로 동작합니다.

## 핵심 철학

```
결과물 ≠ 목표. 결과물 = 목표 달성을 위한 수단.
```

## 프로젝트 구조

```
orchestrator/SKILL.md              → 프로젝트 시작점, 워크플로우 조율
agents/{team}/{agent}/SKILL.md     → 개별 에이전트 정의
agents/_teams/{team}/TEAM_KNOWLEDGE.md → 팀 공유 지식
templates/                         → PRD, 핸드오프, 상태 파일 템플릿
projects/                          → 프로젝트별 산출물
```

## 팀 구성

| 팀 | 에이전트 | 역할 |
|----|---------|------|
| **Strategy** | PMF Planner, Feature Planner, Policy Architect, Data Analyst, Business Strategist, Idea Refiner, Scope Estimator | 전략, 기획, 분석 |
| **Growth** | GTM Strategist, Content Writer, Brand Marketer, Paid Marketer | 마케팅, 브랜딩 |
| **Experience** | User Researcher, Desk Researcher, UX Designer, UI Designer | 리서치, 디자인 |
| **Engineering** | Creative Frontend, FDE, Architect, Backend Developer, API Developer, Data Collector, Data Engineer, Cloud Admin | 개발, 인프라 |

## 멀티 세션 실행 규칙

### Orchestrator 세션 (이 세션)
1. `orchestrator/SKILL.md` 로드
2. 사용자 아이디어 → 구체화 질문 → PRD 생성
3. `projects/{id}/_status.yaml` 생성
4. 팀별 세션 컨텍스트(`sessions/`) 생성
5. 각 Phase별 실행할 팀 세션 안내
6. 세션 완료 후 `_status.yaml` + `_handoff.md` 확인

### 팀 세션 (개별 터미널)
1. `projects/{id}/sessions/{team}/CLAUDE.md` 읽기
2. 이전 단계 `_handoff.md` 확인
3. 해당 에이전트 `SKILL.md` 로드하여 작업 수행
4. 산출물을 `projects/{id}/stage-N-{name}/`에 저장
5. `_handoff.md` 작성 (다음 에이전트에게 맥락 전달)
6. `_status.yaml`의 해당 stage를 `completed`로 업데이트

## 핸드오프 프로토콜

모든 에이전트는 작업 완료 시 `_handoff.md`를 작성합니다:
- **Summary**: 핵심 발견/결정 3줄 요약
- **Artifacts**: 생성된 산출물 목록
- **Key Decisions**: 결정 사항과 근거
- **Context for Next Agent**: 다음 에이전트가 알아야 할 맥락
- **Open Questions**: 미해결 질문

템플릿: `templates/handoff.md`

## 상태 추적

`projects/{id}/_status.yaml`로 전체 워크플로우를 추적합니다:
- `pending` → `in_progress` → `completed`
- `needs_revision`: 이전 stage 수정으로 재생성 필요

템플릿: `templates/status.yaml`

## 워크플로우 타입

| 타입 | 용도 | 핵심 Phase |
|------|------|-----------|
| PMF 탐색 | 새 제품 시장 적합성 | Research → Planning → Design → Build → Launch |
| 기능 확장 | 기존 제품 기능 추가 | Analysis → Planning → Design → Build |
| 리브랜딩 | 브랜드 재정립 | Research → Branding → Design → Marketing |
| 빠른 프로토타입 | 최소 기능 검증 | Refine → Build → Launch |
