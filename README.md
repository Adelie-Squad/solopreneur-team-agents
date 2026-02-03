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
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── orchestrator/
│   └── SKILL.md              # 메인 오케스트레이터
├── agents/
│   ├── _teams/               # 팀별 공유 지식
│   │   ├── strategy/
│   │   │   └── TEAM_KNOWLEDGE.md
│   │   ├── growth/
│   │   │   └── TEAM_KNOWLEDGE.md
│   │   ├── experience/
│   │   │   └── TEAM_KNOWLEDGE.md
│   │   └── engineering/
│   │       └── TEAM_KNOWLEDGE.md
│   │
│   ├── strategy/             # 전략팀 에이전트
│   │   ├── pmf-planner/
│   │   ├── feature-planner/
│   │   ├── policy-architect/
│   │   ├── data-analyst/
│   │   ├── business-strategist/
│   │   ├── idea-refiner/
│   │   └── scope-estimator/
│   │
│   ├── growth/               # 그로스팀 에이전트
│   │   ├── gtm-strategist/
│   │   ├── content-writer/
│   │   ├── brand-marketer/
│   │   └── paid-marketer/
│   │
│   ├── experience/           # 경험팀 에이전트
│   │   ├── user-researcher/
│   │   ├── desk-researcher/
│   │   ├── ux-designer/
│   │   └── ui-designer/
│   │
│   └── engineering/          # 엔지니어링팀 에이전트
│       ├── creative-frontend/
│       ├── fde/
│       ├── architect/
│       ├── backend-developer/
│       ├── api-developer/
│       ├── data-collector/
│       ├── data-engineer/
│       └── cloud-admin/
│
├── templates/
│   ├── prd-pmf.md            # PMF 탐색용 PRD
│   ├── prd-experiment.md     # 가설 검증용 PRD
│   ├── prd-feature.md        # 기능 확장용 PRD
│   └── questions.md          # 구체화 질문 템플릿
│
└── projects/
    └── .gitkeep              # 프로젝트 저장 위치
```

## 사용법

### 1. 설치

```bash
# Claude Code Skills 디렉토리에 복사
cp -r solo-founder-agents/* ~/.claude/skills/

# 또는 심볼릭 링크
ln -s $(pwd)/solo-founder-agents ~/.claude/skills/solo-founder
```

### 2. 프로젝트 시작

```
새 프로젝트 시작해줘.
"전세사기 예방 서비스 - 임차인이 쉽게 위험도 체크"
```

### 3. 에이전트 직접 호출

```
아이디어 구체화해줘 - AI 기반 식단 관리 앱
→ Idea Refiner 에이전트 활성화

사용자 인터뷰 가이드 만들어줘
→ User Researcher 에이전트 활성화

GTM 전략 세워줘
→ GTM Strategist 에이전트 활성화
```

### 4. 팀 협업

각 에이전트는 필요에 따라 다른 팀/에이전트에 Handoff합니다.

```yaml
# 예: PMF Planner의 Handoff
next_agents:
  - feature-planner: MVP 기능 상세화
  - user-researcher: 가설 검증 리서치
  - scope-estimator: 개발 일정 산정
```

## 프로젝트 타입별 워크플로우

### Type A: PMF 탐색 (0→1)
```
Idea Refiner → PMF Planner → User Researcher → Feature Planner
    → UX Designer → UI Designer → FDE → GTM Strategist
```

### Type B: 기능 확장
```
Data Analyst → Feature Planner → UX Designer → UI Designer
    → Creative Frontend → Backend Developer
```

### Type C: 리브랜딩
```
Desk Researcher → Brand Marketer → UI Designer → Content Writer
```

### Type D: 빠른 프로토타입
```
Idea Refiner → FDE → GTM Strategist
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
