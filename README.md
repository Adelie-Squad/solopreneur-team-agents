# solopreneur-agents

> git clone → .env 작성 → python setup.py → 끝

24/7 AI 비서 시스템. 제품별 Discord 서버에 자동 보고하고, 명령을 받아 Claude Code를 실행한다.

---

## 설치 (3단계)

### 1. 클론
```bash
git clone https://github.com/your-org/solopreneur-agents
cd solopreneur-agents
```

### 2. .env 작성
```bash
cp .env.example .env
# .env 파일 열어서 4개 값만 채우기:
# OWNER_NAME, OWNER_ROLE, DISCORD_TOKEN, REPOS_BASE_PATH
```

### 3. 설치 실행
```bash
python setup.py
```

Docker가 있으면 나머지는 자동이다. 끝.

---

## 전제 조건

| 항목 | 설치 링크 |
|------|-----------|
| Docker Desktop | https://docs.docker.com/desktop/ |
| Python 3.10+ | https://python.org (대부분 이미 설치됨) |

Windows / Mac / Linux 동일하게 동작한다.

---

## 사용법

### Discord에서 명령하기
봇을 초대한 서버의 `#owner-command` 채널에 메시지를 보내면 Claude Code가 응답한다.

```
너: 랜딩페이지 카피 초안 써줘
봇: [제품명] ...
```

### 새 프로젝트 생성
```bash
python cli/new_project.py
```
인터랙티브 UI가 나타나고, 선택만 하면 디렉토리 + CLAUDE.md + GitHub 레포가 자동 생성된다.

### 전체 현황 확인
```bash
python cli/status.py
```

### 프로젝트 디렉토리에서 Claude Code 실행
```bash
cd ~/repos/my-product/projects/pmf-validation
claude
# CLAUDE.md가 자동 로딩되어 컨텍스트 격리된 상태로 시작됨
```

---

## 자동 루틴 스케줄 (KST)

| 시간 | 루틴 | 보고 채널 |
|------|------|-----------|
| 06:00 매일 | Morning Brief | `#daily-brief` |
| 12:00 매일 | Signal Scan | `#signals` |
| 16:00 매일 | Experiment Check | `#experiments` |
| 22:00 매일 | Daily Log | `#daily-brief` |
| 일 20:00 | Weekly Review | `#weekly-review` |

---

## 구조

```
solopreneur-agents/        ← 이 레포 (Universal Core)
├── setup.py               ← 설치 마법사
├── docker-compose.yml     ← 크로스플랫폼 실행
├── core/
│   ├── OWNER.md           ← 오너 프로필 (공유)
│   ├── PRINCIPLES.md      ← 의사결정 원칙 (공유)
│   ├── VOICE.md           ← 글쓰기 스타일 (공유)
│   └── products.json      ← setup.py가 자동 생성
├── routines/              ← 루틴 프롬프트 (수정 가능)
├── src/
│   ├── bot.py             ← Discord 봇
│   └── scheduler.py       ← 24시간 루틴 실행기
├── cli/
│   ├── new_project.py     ← 프로젝트 생성
│   └── status.py          ← 현황 대시보드
├── orchestrator/
│   └── SKILL.md           ← 프로젝트 워크플로우 조율
├── agents/                ← 27개 전문 에이전트
│   ├── _teams/            ← 팀별 공유 지식
│   ├── strategy/          ← 전략팀 (7 agents)
│   ├── growth/            ← 그로스팀 (4 agents)
│   ├── experience/        ← 경험팀 (4 agents)
│   └── engineering/       ← 엔지니어링팀 (8 agents)
└── templates/             ← PRD, 핸드오프, 상태 템플릿

~/repos/                   ← REPOS_BASE_PATH (별도)
├── my-product/            ← 제품 레이어 (Layer 1)
│   ├── CLAUDE.md
│   ├── product/
│   ├── memory/
│   └── projects/          ← 프로젝트 레이어 (Layer 2)
│       └── pmf-validation/
│           ├── CLAUDE.md  ← 자동 생성됨
│           └── ...
└── another-product/
    └── ...
```

---

## 팀 기반 에이전트 (27개)

| 팀 | 에이전트 | 역할 |
|----|---------|------|
| **Strategy** | PMF Planner, Feature Planner, Policy Architect, Data Analyst, Business Strategist, Idea Refiner, Scope Estimator | 전략, 기획, 분석 |
| **Growth** | GTM Strategist, Content Writer, Brand Marketer, Paid Marketer | 마케팅, 브랜딩 |
| **Experience** | User Researcher, Desk Researcher, UX Designer, UI Designer | 리서치, 디자인 |
| **Engineering** | Creative Frontend, FDE, Architect, Backend Developer, API Developer, Data Collector, Data Engineer, Cloud Admin | 개발, 인프라 |

---

## 시스템 관리

```bash
# 재시작
docker compose restart

# 로그 확인
docker compose logs -f

# 중지
docker compose down

# 업데이트 후 재빌드
git pull && docker compose build && docker compose up -d
```

---

## 루틴 커스터마이징

`routines/` 폴더의 `.md` 파일을 수정하면 된다. 재빌드 불필요.

```bash
# 예: Morning Brief 프롬프트 수정
code routines/morning-brief.md
docker compose restart scheduler
```

---

## FAQ

**Q: Windows에서 경로 구분자 문제?**
A: `REPOS_BASE_PATH`에 `/` 슬래시 사용. Docker가 변환해준다.

**Q: Claude Code 인증은?**
A: Docker 컨테이너 안에서 Claude Code 로그인 필요.
`docker compose exec bot claude` 실행 후 한 번만 로그인.

**Q: 제품을 나중에 추가하려면?**
A: `python setup.py` 재실행 → 기존 설정 유지하고 제품만 추가.

**Q: 루틴 시간대가 다르면?**
A: `docker-compose.yml`의 `TZ` 환경변수 수정.

---

## Contributing

1. Fork this repository
2. Create your feature branch
3. Submit a pull request

자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

## License

MIT License

---

Made with Claude for solo founders who build with AI
