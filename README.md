# Solo Founder Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blueviolet)](https://claude.ai)

**1인 창업자를 위한 AI 에이전트 협업 시스템**

Claude Code + Skills 기반으로 기획, 리서치, 브랜딩, 디자인, 개발, 마케팅을 자동화합니다.

> **Prerequisites**: [Claude Code](https://claude.ai) 환경에서 Skills 시스템을 활용합니다.

## 핵심 철학

> "결과물은 목표가 아니라 수단이다."

- MVP는 목표가 아닙니다. **PMF를 찾는 것**이 목표입니다.
- 랜딩 페이지는 목표가 아닙니다. **가설을 검증하는 것**이 목표입니다.
- PRD는 목표가 아닙니다. **팀을 정렬시키는 것**이 목표입니다.

## 팀 기반 에이전트 구조

직무 간 경계가 흐려지는 시대에 맞춰, **목표 중심의 세분화된 에이전트**와 **팀 단위 협업 구조**를 설계했습니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    TEAM-BASED STRUCTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Strategy   │  │   Growth    │  │ Experience  │         │
│  │    Team     │←→│    Team     │←→│    Team     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         ↑                                    ↑              │
│         └────────────────┬───────────────────┘              │
│                          ↓                                   │
│                  ┌─────────────┐                            │
│                  │ Engineering │                            │
│                  │    Team     │                            │
│                  └─────────────┘                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 팀별 구성

각 팀은 **공유 지식(TEAM_KNOWLEDGE.md)**을 가지며, 팀원(에이전트)은 이를 참조합니다.

#### Strategy Team (전략팀)
제품 전략, 기획, 분석을 담당합니다.

| 에이전트 | 역할 |
|----------|------|
| **PMF Planner** | 0→1 단계 PMF 탐색, 가설 수립 |
| **Feature Planner** | 기능 추가/개선 기획 |
| **Policy Architect** | 정책 설계 (회원, 권한, 결제 등) |
| **Data Analyst** | GA/도메인 데이터 분석, 인사이트 도출 |
| **Business Strategist** | 사업/전략 기획, 비즈니스 모델 |
| **Idea Refiner** | 아이디어 구체화 및 고도화 |
| **Scope Estimator** | 개발 범위 및 일정 기획 |

#### Growth Team (그로스팀)
사용자 획득, 마케팅, 브랜딩을 담당합니다.

| 에이전트 | 역할 |
|----------|------|
| **GTM Strategist** | Go-To-Market 전략 |
| **Content Writer** | 콘텐츠 카피라이팅 |
| **Brand Marketer** | 브랜딩, 톤앤매너, 브랜드 전략 |
| **Paid Marketer** | 페이드 마케팅, 광고 최적화 |

#### Experience Team (경험팀)
사용자 리서치, UX/UI 디자인을 담당합니다.

| 에이전트 | 역할 |
|----------|------|
| **User Researcher** | 디자인씽킹 기반 유저 리서치 |
| **Desk Researcher** | 시장/경쟁/레퍼런스 리서치 |
| **UX Designer** | 사용자 경험, 플로우, IA 설계 |
| **UI Designer** | 비주얼 디자인, 디자인 시스템 |

#### Engineering Team (엔지니어링팀)
소프트웨어 개발, 데이터 엔지니어링, 인프라를 담당합니다.

| 에이전트 | 역할 |
|----------|------|
| **Creative Frontend** | 인터랙티브 프론트엔드 개발 |
| **FDE (Forward Deployed Engineer)** | 빠른 프로토타입, E2E 개발 |
| **Architect** | 시스템 아키텍처 설계 |
| **Backend Developer** | 서버/비즈니스 로직 개발 |
| **API Developer** | API 설계 및 문서화 |
| **Data Collector** | 데이터 수집 파이프라인 |
| **Data Engineer** | 데이터 정제/변환/가공 |
| **Cloud Admin** | 클라우드 인프라 관리 |

## 팀 간 협업

각 에이전트는 명확한 **R&R (Role & Responsibility)**을 가지면서도, 팀 공유 지식을 통해 시너지를 냅니다.

```
예: GTM 전략 수립 시

[GTM Strategist] ← 채널 전략 수립
       ↓
[Paid Marketer] ← SNS별 특성 고려한 광고 전략
       ↓
[Content Writer] ← SNS별 사용자 특성에 맞는 콘텐츠
       ↑
[Growth Team KNOWLEDGE] ← 채널별 특성, 톤앤매너 공유
```

## 디렉토리 구조

```
solo-founder-agents/
├── CLAUDE.md                    # 세션 자동 컨텍스트
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── orchestrator/
│   └── SKILL.md                 # 메인 오케스트레이터
├── agents/
│   ├── _teams/                  # 팀별 공유 지식
│   │   ├── strategy/TEAM_KNOWLEDGE.md
│   │   ├── growth/TEAM_KNOWLEDGE.md
│   │   ├── experience/TEAM_KNOWLEDGE.md
│   │   └── engineering/TEAM_KNOWLEDGE.md
│   ├── strategy/                # 전략팀 (7 agents)
│   ├── growth/                  # 그로스팀 (4 agents)
│   ├── experience/              # 경험팀 (4 agents)
│   └── engineering/             # 엔지니어링팀 (8 agents)
│
├── templates/
│   ├── prd-pmf.md               # PMF 탐색용 PRD
│   ├── prd-experiment.md        # 가설 검증용 PRD
│   ├── prd-feature.md           # 기능 확장용 PRD
│   ├── questions.md             # 구체화 질문 템플릿
│   ├── handoff.md               # 핸드오프 파일 템플릿
│   ├── status.yaml              # 워크플로우 상태 템플릿
│   ├── session-orchestrator.md  # Orchestrator 세션 컨텍스트
│   ├── session-strategy.md      # Strategy 팀 세션 컨텍스트
│   ├── session-experience.md    # Experience 팀 세션 컨텍스트
│   ├── session-growth.md        # Growth 팀 세션 컨텍스트
│   └── session-engineering.md   # Engineering 팀 세션 컨텍스트
│
├── scripts/
│   ├── init-project.sh          # 프로젝트 초기화
│   └── start-session.sh         # 팀 세션 시작
│
├── docs/
│   └── 구조-개선안-멀티세션-팀-조율.md
│
└── projects/                    # 프로젝트 산출물
    └── {project_id}/
        ├── _status.yaml         # 워크플로우 상태
        ├── _changelog.md        # 변경 이력
        ├── prd.md               # PRD
        ├── sessions/            # 팀별 세션 컨텍스트
        │   ├── orchestrator/CLAUDE.md
        │   ├── strategy/CLAUDE.md
        │   ├── experience/CLAUDE.md
        │   ├── growth/CLAUDE.md
        │   └── engineering/CLAUDE.md
        ├── stage-1-research/
        │   ├── _handoff.md      # 다음 에이전트 맥락 전달
        │   └── *.md             # 산출물
        ├── stage-2-planning/
        ├── stage-3-design/
        ├── stage-4-development/
        └── stage-5-marketing/
```

## 사용법

### 1. 설치

```bash
# Claude Code Skills 디렉토리에 복사
cp -r solo-founder-agents/* ~/.claude/skills/

# 또는 심볼릭 링크
ln -s $(pwd)/solo-founder-agents ~/.claude/skills/solo-founder
```

### 2. 프로젝트 시작 (Orchestrator 세션)

```bash
# 터미널 1: Orchestrator 세션
cd solo-founder-agents
claude
```

```
새 프로젝트 시작해줘.
"전세사기 예방 서비스 - 임차인이 쉽게 위험도 체크"
```

PRD 승인 후 프로젝트가 초기화됩니다. 스크립트로도 초기화 가능:

```bash
./scripts/init-project.sh jeonse-guard "전세사기 예방 서비스" pmf
```

### 3. 팀 세션 실행 (멀티 세션)

Orchestrator가 안내하는 Phase별로 팀 세션을 병렬 실행합니다:

```bash
# 터미널 2: Experience Team (Research)
./scripts/start-session.sh jeonse-guard experience

# 터미널 3: Strategy Team (Idea Refinement) - 동시 실행
./scripts/start-session.sh jeonse-guard strategy
```

### 4. 핸드오프 기반 협업

각 에이전트는 완료 시 `_handoff.md`를 작성하여 다음 에이전트에게 맥락을 전달합니다:

```
stage-1-research/_handoff.md
→ Summary, Key Decisions, Context for Next Agent
→ 다음 Phase의 에이전트가 이 파일을 읽고 작업 시작
```

### 5. 에이전트 직접 호출

개별 에이전트도 독립적으로 호출 가능합니다:

```
아이디어 구체화해줘 - AI 기반 식단 관리 앱
→ Idea Refiner 에이전트 활성화

사용자 인터뷰 가이드 만들어줘
→ User Researcher 에이전트 활성화
```

## 프로젝트 타입별 워크플로우 (병렬 실행)

### Type A: PMF 탐색 (0→1)
```
Phase 1 (병렬): [Experience] Research  +  [Strategy] Idea Refine
Phase 2 (병렬): [Strategy] Planning   +  [Growth] Branding*
Phase 3:        [Experience] Design
Phase 4 (병렬): [Engineering] Build   +  [Growth] Marketing
Phase 5:        [Growth] Launch
                                        * 브랜드 중요도 HIGH인 경우
```

### Type B: 기능 확장
```
Phase 1: [Strategy] Analysis
Phase 2: [Strategy] Planning
Phase 3: [Experience] Design
Phase 4: [Engineering] Build
```

### Type C: 리브랜딩
```
Phase 1: [Experience] Research
Phase 2: [Growth] Branding → [Experience] Design
Phase 3: [Growth] Marketing
```

### Type D: 빠른 프로토타입
```
Phase 1: [Strategy] Idea Refine
Phase 2: [Engineering] Build
Phase 3: [Growth] Launch
```

## 커스터마이징

### 새 에이전트 추가

`agents/{team}/{agent-name}/SKILL.md` 생성:

```markdown
# Agent Name

> 한 줄 설명

## Team
{Team} Team (`../_teams/{team}/TEAM_KNOWLEDGE.md` 참조)

## R&R (Role & Responsibility)
### 담당 범위
### 담당하지 않는 것

## Trigger
## Input
## Process
## Output
## Quality Checklist
## Collaboration
## Handoff
```

### 팀 지식 확장

`agents/_teams/{team}/TEAM_KNOWLEDGE.md`에 공유 프레임워크, 템플릿, 용어집 추가

## Contributing

1. Fork this repository
2. Create your feature branch
3. Add/modify agents or team knowledge
4. Submit a pull request

자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

## License

MIT License - 자유롭게 사용, 수정, 배포하세요.

---

Made with Claude for solo founders who build with AI
