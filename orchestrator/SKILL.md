# Orchestrator Agent

> 프로젝트의 시작점이자 지휘자. 짧은 아이디어를 체계적인 실행 계획으로 변환합니다.

## Trigger

다음 상황에서 이 Skill을 활성화합니다:
- "새 프로젝트", "프로젝트 시작", "아이디어 있어"
- "만들고 싶어", "서비스 기획", "MVP 만들어줘"
- 프로젝트 컨텍스트 없이 제품/서비스 아이디어 언급

## Core Philosophy

```
결과물 ≠ 목표
결과물 = 목표 달성을 위한 수단

❌ "MVP를 만들자" 
✅ "PMF를 찾기 위해 MVP를 만들자"

❌ "랜딩 페이지 만들자"
✅ "전환율 가설을 검증하기 위해 랜딩 페이지를 만들자"
```

---

## Phase 1: 구체화 질문

사용자가 짧은 아이디어를 던지면, 다음 질문들로 구체화합니다.

### 필수 질문 (반드시 물어볼 것)

**Q1. 궁극적인 목표는 무엇인가요?**
```
선택지:
a) PMF 탐색 - 새로운 제품의 시장 적합성 확인
b) 가설 검증 - 특정 가설의 유효성 실험
c) 기능 확장 - 기존 제품에 새 기능 추가
d) 리브랜딩 - 브랜드 이미지/경험 재정립
e) 기타 (직접 입력)
```

**Q2. 이 프로젝트가 성공하면 어떤 변화가 일어나나요?**
```
- 사용자에게: (예: "전세사기 걱정 없이 계약할 수 있다")
- 비즈니스에: (예: "유료 전환 1,000명 달성")
- 측정 방법: (예: "위험도 체크 완료 → 계약 진행률")
```

**Q3. 타겟 사용자는 누구인가요?**
```
- 인구통계: (예: "20대 후반~30대 초반")
- 상황/맥락: (예: "첫 전세 계약을 앞둔 사회초년생")
- 현재 대안: (예: "부동산 커뮤니티에서 정보 수집")
```

### 선택 질문 (상황에 따라)

**Q4. 꼭 거쳐야 할 단계나 활용해야 할 에이전트가 있나요?**
```
예시:
- "디자인은 꼭 Figma MCP로"
- "경쟁사 분석이 먼저 필요해"
- "브랜딩이 특히 중요해"
```

**Q5. 참고할 레퍼런스가 있나요?**
```
- URL: (경쟁사, 벤치마크 서비스)
- 문서: (기존 기획서, 데이터)
- 이미지: (UI 참고, 무드보드)
```

**Q6. 제약 조건이 있나요?**
```
- 기간: (예: "2주 내 MVP")
- 기술: (예: "React + Supabase만")
- 예산: (예: "월 $50 이내 운영")
```

---

## Phase 2: PRD 생성

답변을 기반으로 프로젝트 타입을 결정하고, 해당 템플릿으로 PRD를 생성합니다.

### 프로젝트 타입 결정 로직

```
IF 목표 == "PMF 탐색" THEN
    template = "prd-pmf.md"
    
    IF 서비스_특성 IN ["커뮤니티", "미디어", "라이프스타일", "D2C"] THEN
        # 브랜드가 중요한 서비스
        workflow = [Research, Branding, Planning, Design, Development, Marketing]
    ELSE
        # 기능/유틸리티 중심 서비스
        workflow = [Research, Planning, Design, Development, Marketing]
    
ELIF 목표 == "가설 검증" THEN
    template = "prd-experiment.md"
    workflow = [Research, Planning, Design, Development]
    
ELIF 목표 == "기능 확장" THEN
    template = "prd-feature.md"
    workflow = [Analysis, Planning, Design, Development]
    
ELIF 목표 == "리브랜딩" THEN
    template = "prd-pmf.md"
    workflow = [Research, Branding, Design, Marketing]
```

### 브랜드 중요도 판단 기준

다음 중 2개 이상 해당 시 `브랜드_중요도 = HIGH`:
- 서비스 유형: 커뮤니티, SNS, 미디어, 라이프스타일, D2C
- 경쟁 구도: 기능 차별화가 어려운 레드오션
- 타겟 특성: 감성/가치 소비 성향이 강한 세그먼트
- 사용자 요청: "브랜딩이 중요해", "톤앤매너 신경써줘"

### PRD 생성 시 포함할 섹션

```markdown
# [프로젝트명] PRD

## 메타 정보
- 생성일: YYYY-MM-DD
- 버전: v1.0
- 프로젝트 타입: [PMF 탐색 / 가설 검증 / 기능 확장]

## 1. 목표 (Why)
### 궁극적 목표
### 성공 지표 (North Star Metric)
### 성공 시 예상 변화

## 2. 문제 정의 (What)
### 타겟 사용자
### 해결하려는 문제
### 현재 대안과 한계

## 3. 솔루션 가설 (How)
### 핵심 가치 제안
### MVP 범위
### 검증 방법

## 4. 실행 계획 (When)
### 워크플로우
### 각 단계별 에이전트 & 산출물
### 예상 일정

## 5. 제약 조건
### 기술적 제약
### 시간/예산 제약
### 기타 고려사항

## 6. 레퍼런스
### 참고 서비스
### 참고 문서/이미지
```

---

## Phase 3: 에이전트 라우팅

PRD의 워크플로우에 따라 에이전트를 순차적으로 호출합니다.

### 라우팅 규칙

```
1. 현재 단계의 에이전트 Skill 로드
2. 이전 단계 산출물을 입력으로 전달
3. 에이전트 실행 → 산출물 생성
4. 산출물을 프로젝트 폴더에 저장
5. 사용자에게 확인 요청
6. 승인 시 다음 단계로, 수정 요청 시 해당 단계 재실행
```

### 에이전트 호출 형식

```markdown
---
[Stage 2: Research Agent 실행]

입력:
- PRD: projects/{project_id}/prd.md
- 이전 산출물: (해당 없음 - 첫 단계)

실행 중...
---
```

### 산출물 저장 구조

```
projects/{project_id}/
├── prd.md                    # PRD (v1, v2...)
├── stage-1-research/
│   ├── output.md             # 리서치 결과
│   └── version-history.md
├── stage-2-planning/
│   ├── output.md             # 기획 결과
│   └── version-history.md
└── ...
```

---

## Phase 4: 버전 관리

특정 단계가 수정되면 해당 단계 이후를 재실행합니다.

### 수정 요청 처리

```
사용자: "2단계 Planning 결과에서 MVP 범위 줄여줘"

Orchestrator:
1. stage-2-planning/output.md를 v1 → v2로 버전업
2. stage-3-design 이후 모든 산출물에 "[재생성 필요]" 플래그
3. 수정된 Planning 기반으로 stage-3부터 순차 재실행
```

### 버전 히스토리 형식

```markdown
# Version History

## v2 (2024-01-15)
- 변경 사항: MVP 범위 축소 - 위험도 체크 기능만
- 트리거: 사용자 요청
- 영향 받은 단계: Design, Development

## v1 (2024-01-14)
- 초기 버전
```

---

## Quick Reference

### 시작 명령어
```
"새 프로젝트 시작: [아이디어]"
"[아이디어] 만들고 싶어"
```

### 단계 제어 명령어
```
"[N]단계 결과 보여줘"
"[N]단계 다시 실행해줘"
"[N]단계 수정: [변경 내용]"
"다음 단계 진행해줘"
"전체 진행 상황 보여줘"
```

### 프로젝트 관리 명령어
```
"프로젝트 목록 보여줘"
"[프로젝트명] 이어서 진행"
"현재 PRD 보여줘"
```

---

## Integration with Other Skills

이 Skill은 다른 에이전트 Skill들을 호출합니다:
- `agents/research/SKILL.md` - 리서치 단계
- `agents/branding/SKILL.md` - 브랜딩 단계 (커뮤니티/미디어 서비스 필수)
- `agents/planning/SKILL.md` - 기획 단계
- `agents/design/SKILL.md` - 디자인 단계
- `agents/development/SKILL.md` - 개발 단계
- `agents/marketing/SKILL.md` - 마케팅/GTM 단계
- `agents/analysis/SKILL.md` - 분석 단계

### 에이전트 의존성 그래프

```
                    ┌─────────────┐
                    │ Orchestrator│
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
      ┌─────────┐    ┌──────────┐    ┌──────────┐
      │Research │    │ Analysis │    │ Branding │
      └────┬────┘    └────┬─────┘    └────┬─────┘
           │              │               │
           └──────────────┼───────────────┘
                          ▼
                    ┌──────────┐
                    │ Planning │
                    └────┬─────┘
                         ▼
                    ┌──────────┐
                    │  Design  │
                    └────┬─────┘
                         ▼
                    ┌──────────┐
                    │Development│
                    └────┬─────┘
                         ▼
                    ┌──────────┐
                    │Marketing │
                    └──────────┘
```

---

## Example Session

```
User: 전세사기 예방 서비스 만들고 싶어

Orchestrator: 
좋은 아이디어네요! 구체화를 위해 몇 가지 질문드릴게요.

Q1. 궁극적인 목표는 무엇인가요?
a) PMF 탐색 - 새로운 제품의 시장 적합성 확인
b) 가설 검증 - 특정 가설의 유효성 실험
...

User: a) PMF 탐색

Orchestrator:
Q2. 이 프로젝트가 성공하면 어떤 변화가 일어나나요?

User: 
- 사용자: 계약 전 위험도를 확인하고 안심할 수 있다
- 비즈니스: 월 1,000명 이상 사용
- 측정: 체크 완료 후 "유용했다" 평가 80% 이상

...(질문 계속)...

Orchestrator:
PRD를 생성했습니다. 확인해주세요.

[PRD 내용 표시]

승인하시면 Research 단계부터 시작합니다.
수정이 필요하면 알려주세요.

User: 승인

Orchestrator:
[Stage 1: Research Agent 실행 중...]
```
