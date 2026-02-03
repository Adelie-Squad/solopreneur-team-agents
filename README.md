# Solo Founder Agents 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blueviolet)](https://claude.ai)

**1인 창업자를 위한 AI 에이전트 협업 시스템**

Claude Code + Skills 기반으로 기획, 리서치, 브랜딩, 디자인, 개발, 마케팅을 자동화합니다.

> 💡 **Prerequisites**: [Claude Code](https://claude.ai) 환경에서 Skills 시스템을 활용합니다.

## 핵심 철학

> "결과물은 목표가 아니라 수단이다."

- MVP는 목표가 아닙니다. **PMF를 찾는 것**이 목표입니다.
- 랜딩 페이지는 목표가 아닙니다. **가설을 검증하는 것**이 목표입니다.
- PRD는 목표가 아닙니다. **팀을 정렬시키는 것**이 목표입니다.

## 작동 방식

```
┌─────────────────────────────────────────────────────────────┐
│  "전세사기 예방 서비스 만들고 싶어"                            │
│                         ↓                                   │
│  [Orchestrator] 구체화 질문 3-5개 생성                        │
│                         ↓                                   │
│  사용자 답변 → PRD 자동 생성                                  │
│                         ↓                                   │
│  목표에 따라 필요한 에이전트 자동 라우팅                        │
│                         ↓                                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │Research │→│Planning │→│ Design  │→│  Dev    │           │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘           │
│                         ↓                                   │
│  각 단계별 산출물 → 다음 단계 입력                            │
│                         ↓                                   │
│  [버전 관리] 수정 시 해당 단계 이후 재실행                     │
└─────────────────────────────────────────────────────────────┘
```

## 설치

```bash
# Claude Code Skills 디렉토리에 복사
cp -r solo-founder-agents/* ~/.claude/skills/

# 또는 심볼릭 링크
ln -s $(pwd)/solo-founder-agents ~/.claude/skills/solo-founder
```

## 사용법

### 1. 새 프로젝트 시작

Claude Code에서:
```
새 프로젝트 시작해줘. 
"전세사기 예방 서비스 - 임차인이 쉽게 위험도 체크"
```

### 2. 구체화 질문에 답변

Orchestrator가 자동으로 질문합니다:
- 궁극적인 목표는? (PMF 탐색 / 가설 검증 / 기능 확장 등)
- 타겟 사용자는?
- 성공 지표는?
- 필수로 거쳐야 할 단계가 있나요?
- 참고할 레퍼런스가 있나요?

### 3. 자동 실행

답변 기반으로 PRD가 생성되고, 필요한 에이전트가 순차적으로 실행됩니다.

### 4. 중간 수정

```
2단계 리서치 결과 수정해줘.
타겟을 "20대"에서 "30대 신혼부부"로 바꿔.
```
→ 2단계 이후 모든 산출물이 새 버전으로 재생성됩니다.

## 에이전트 목록

| 에이전트 | 역할 | 주요 산출물 |
|----------|------|------------|
| **Orchestrator** | 프로젝트 시작, PRD 생성, 에이전트 라우팅 | PRD, 프로젝트 상태 |
| **Research** | 시장/경쟁/유저 리서치 | 리서치 리포트, 페르소나 |
| **Branding** | 브랜드 전략, 톤앤매너, 비주얼 방향 | 브랜드 가이드, 메시지 |
| **Planning** | 기능 정의, 우선순위, 로드맵 | 기능 명세, MVP 범위 |
| **Design** | UI/UX, 와이어프레임, 디자인 시스템 | 와이어프레임, 컴포넌트 |
| **Development** | 코드 생성, 아키텍처 | 소스 코드, API 명세 |
| **Marketing** | GTM, 카피, 런칭 전략 | 랜딩 카피, GTM 전략 |
| **Analysis** | 데이터 분석, 지표 설계 | 대시보드, 인사이트 |

## 프로젝트 타입별 워크플로우

### Type A: PMF 탐색 - 유틸리티/기능 중심
```
Research → Planning → Design → Development → Marketing(GTM)
          ↑__________________|  (PMF 미확인 시 반복)
```

### Type B: PMF 탐색 - 브랜드/커뮤니티 중심
```
Research → Branding → Planning → Design → Development → Marketing(GTM)
```

### Type C: 가설 검증 (실험)
```
Research → Planning → Design → Development
     ↑___________________________|  (결과 기반 반복)
```

### Type D: 기능 확장 (기존 제품)
```
Analysis → Planning → Design → Development
```

### Type E: 리브랜딩
```
Research → Branding → Design → Marketing
```

## 디렉토리 구조

```
solo-founder-agents/
├── README.md
├── LICENSE
├── .gitignore
├── orchestrator/
│   └── SKILL.md          # 메인 오케스트레이터
├── agents/
│   ├── research/
│   │   └── SKILL.md      # 리서치 에이전트
│   ├── branding/
│   │   └── SKILL.md      # 브랜딩 에이전트 ⭐
│   ├── planning/
│   │   └── SKILL.md      # 기획 에이전트
│   ├── design/
│   │   └── SKILL.md      # 디자인 에이전트
│   ├── development/
│   │   └── SKILL.md      # 개발 에이전트
│   ├── marketing/
│   │   └── SKILL.md      # 마케팅/GTM 에이전트
│   └── analysis/
│       └── SKILL.md      # 분석 에이전트
├── templates/
│   ├── prd-pmf.md        # PMF 탐색용 PRD
│   ├── prd-experiment.md # 가설 검증용 PRD
│   ├── prd-feature.md    # 기능 확장용 PRD
│   └── questions.md      # 구체화 질문 템플릿
└── projects/
    └── .gitkeep          # 실제 프로젝트 저장 위치
```

## 커스터마이징

### 새 에이전트 추가

`agents/your-agent/SKILL.md` 생성:
```markdown
# Your Agent

## Trigger
- "your-keyword" 언급 시 활성화

## Input
- 이전 단계 산출물

## Process
1. 단계 1
2. 단계 2

## Output
- 산출물 형태
```

### PRD 템플릿 커스터마이징

`templates/prd-custom.md`에서 섹션 추가/수정

## Contributing

1. Fork this repository
2. Create your feature branch
3. Add/modify agents or templates
4. Submit a pull request

## License

MIT License - 자유롭게 사용, 수정, 배포하세요.

---

Made with ❤️ for solo founders who build with AI
