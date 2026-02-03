# Contributing to Solo Founder Agents

먼저, 기여해주셔서 감사합니다! 🎉

## 기여 방법

### 1. 새 에이전트 추가

`agents/your-agent/SKILL.md` 파일을 생성합니다.

**필수 섹션:**
```markdown
# [Agent Name]

> 한 줄 설명

## Trigger
- 언제 이 에이전트가 활성화되는가

## Input
- 필수/선택 입력 항목

## Process
- 단계별 처리 로직

## Output
- 산출물 형식

## Quality Checklist
- 품질 검증 기준

## Handoff
- 다음 단계로 전달할 내용
```

### 2. PRD 템플릿 추가

`templates/prd-{type}.md` 파일을 생성합니다.

**템플릿 변수 형식:**
```markdown
{{variable_name}}
```

### 3. 기존 에이전트 개선

1. Fork 후 브랜치 생성
2. 변경 사항 커밋
3. Pull Request 생성

## 코드 스타일

### SKILL.md 작성 원칙

1. **명확한 트리거**: 언제 활성화되는지 구체적으로
2. **구조화된 프로세스**: 단계별로 명확하게
3. **실행 가능한 산출물**: 바로 활용 가능한 형태
4. **품질 체크리스트**: 자가 검증 가능하도록

### 네이밍 규칙

- 에이전트: `lowercase-with-hyphen` (예: `user-research`)
- 템플릿: `prd-{type}.md` (예: `prd-pmf.md`)

## Pull Request 가이드

### PR 제목 형식
```
[Agent] Add branding agent
[Template] Add community PRD template
[Fix] Fix orchestrator routing logic
[Docs] Update README installation guide
```

### PR 설명 포함 사항
- 변경 이유
- 변경 내용 요약
- 테스트 방법 (해당 시)

## 이슈 리포트

버그나 개선 아이디어가 있다면 Issue를 생성해주세요.

### 버그 리포트 템플릿
```
**환경**
- Claude Code 버전:
- OS:

**재현 단계**
1. 
2. 

**예상 동작**

**실제 동작**
```

### 기능 제안 템플릿
```
**문제/필요성**

**제안하는 솔루션**

**대안** (고려한 다른 방법)
```

## 질문이 있으시면

Issue로 질문해주시거나, Discussion을 열어주세요.

---

감사합니다! 🙏
