# SoloSquad 개발 현황 & 로드맵

> 릴리스된 버전, 진행 중인 계획, 결정 로그, 외부 참고자료를 한 자리에 모은 롤링 문서.

**최종 업데이트:** 2026-04-22

---

## 1. 릴리스 현황

### npm에 배포된 버전 (사용 가능)

| 버전 | 날짜 | 주요 내용 | 문서 |
|---|---|---|---|
| `v1.0.0` | 초기 | 코어 구조 | — |
| `v1.1.0` | — | 크로스 플랫폼 (Windows/macOS/Linux) | `v1.1-cross-platform.md` |
| `v1.1.1` | — | QA 하드닝 | `v1.1.1-qa-hardening.md` |
| `v1.1.2` | — | npm 퍼블리시 | `v1.1.2-npm-publish.md` |
| `v1.1.3` | 2026-04-21 | **hotfix** — `dotenv/config` 로드 누락 수정 (`.env` 토큰이 `process.env`로 안 들어가던 문제) | `v1.2.1-messenger-debugging.md` |
| `v1.1.4` | 2026-04-21 | **hotfix** — `solosquad update`의 `package.json` 경로 해석 오류 수정 | 동일 |
| `v1.1.5` | 2026-04-21 | **hotfix** — Windows에서 `claude.cmd` 실행 시 ENOENT (execFile + shell:true) | 동일 |

> v1.1.3~v1.1.5는 메신저 디버깅 문서(`v1.2.1-messenger-debugging.md`)에 담긴 일련의 hotfix 작업 결과.

### 현재 설치 가능 버전: `1.1.5` (npm `latest` 태그)

---

## 2. 진행 중인 계획

### v1.2.2 — GitHub-aligned 계층 구조 재편 (문서 완료, 구현 대기)

**핵심 아이디어:** Workspace / Organization / Repository / Workflow — GitHub 관례와 일치. `REPOS_BASE_PATH` 제거, 단일 트리 루트.

**주요 결정 (2026-04-22):**
- Workspace 루트 이름 자유 (기본 `solosquad`, 페르소나별 여러 개 가능): `solopreneur` / `elon-24-7` / `musk-land` / `moonshot`
- "Product" 디렉토리 폐기 → `.org.yaml`의 `products:` 필드에 메타로만 유지
- "Project" → "Workflow" 이름 변경
- Organization 이름은 사용자 직접 입력 (URL 파싱·API 호출 없음)
- **한 워크스페이스 = 한 메신저 플랫폼 = 한 봇 계정** (v1.1.x의 `MESSENGER=discord,slack` 복수 지정 제거)
- Cross-repo workflow: `_status.yaml`의 각 stage에 `target_repo` 필드

**상태:** 설계 문서 완성. 구현 대기.
**문서:** `docs/v1.2.2-terminology-layout.md`

### v1.2.3 — 마이그레이션 프레임워크 (문서 완료, 구현 대기)

**핵심 아이디어:** 모든 버전 전환에 재사용하는 범용 마이그레이션 시스템. `solosquad migrate` 명령, dry-run 기본, 자동 백업, 다중 버전 체이닝.

**상태:** 설계 문서 완성. v1.2.2와 함께 구현되어야 함 (v1.1.x → v1.2.2 마이그레이션 스크립트가 첫 구체 케이스).
**문서:** `docs/v1.2.3-migration-process.md`

### 실행 순서 (권장)

1. `src/migrations/` 스캐폴딩 구현 (`v1.2.3` Phase 1-2)
2. `src/util/paths.ts` 재작성 (`.solosquad/` 감지) — `v1.2.2` Phase 1
3. `solosquad init` 재작성 — `v1.2.2` Phase 2
4. org/repo loader + `add org`, `add repo`, `sync` — `v1.2.2` Phase 3
5. bot/scheduler/status/doctor 경로 교체 — `v1.2.2` Phase 4
6. Cross-repo workflow runner — `v1.2.2` Phase 5
7. v1.1.x → v1.2.2 마이그레이션 스크립트 + fixture 테스트 — `v1.2.3` Phase 3-4
8. setup-guide·README·architecture 최종 갱신 — `v1.2.2` Phase 6
9. `solosquad@1.2.2` 동시 퍼블리시

**예상 기간:** 2~3주 실 작업 + QA.

---

## 3. 장기 로드맵 (순서 미정)

| 버전 | 주제 | 문서 |
|---|---|---|
| `v1.3.x` | 자율 실행 엔진 | `docs/v1.3-autonomous-engine.md` |
| `v1.4.x` | 스킬 자유도 | `docs/v1.4-skill-freedom.md` |
| `v1.5.x` | 지식 온톨로지 | `docs/v1.5-knowledge-ontology.md` |
| `v1.6.x` | 웹 대시보드 | `docs/v1.6-web-dashboard.md` |

---

## 4. 결정 로그 (주요)

- **2026-04-22** — 한 워크스페이스 = 한 메신저 플랫폼. 복잡한 멀티 어댑터 동시 운영을 단순화. 복수 플랫폼 사용자는 워크스페이스를 여러 개 만들어 분리.
- **2026-04-22** — Organization 자동 clone 기능 제거 (v1.3+로 연기 검토). 사용자가 직접 `git clone`.
- **2026-04-22** — Workspace 루트 이름은 사용자 지정(`.solosquad/` 폴더 감지 기반). 기본 이름 `solosquad`, 페르소나 분리용 다중 루트 허용.
- **2026-04-22** — Windows 기본 경로 `~/Documents/solosquad-repos` 폐기. v1.2.2 단일 트리 루트로 통일.
- **2026-04-21** — 버전 표기는 `vN.N.N` 3자리 고정. 2자리(`v1.2`)는 문서 내 참조 약어로만, 공식 릴리스는 항상 3자리.
- **2026-04-21** — v1.1.3~v1.1.5는 작은 hotfix 연쇄로 빠르게 출시 (dotenv·update·Windows claude.cmd).

---

## 5. 관련 문서

- **아키텍처:** `docs/architecture.md`
- **설치 가이드:** `docs/setup-guide.md`
- **업데이트/마이그레이션 (사용자용):** `docs/upgrade-migration-guide.md`
- **클라우드 배포:** `docs/cloud-deployment.md`
- **메신저 디버깅 (v1.1.3-1.1.5 이력):** `docs/v1.2.1-messenger-debugging.md`
- **안전/보안:** `docs/v1.2-safety-security.md`
- **v1.2.2 구조 재편 스펙:** `docs/v1.2.2-terminology-layout.md`
- **v1.2.3 마이그레이션 프레임워크:** `docs/v1.2.3-migration-process.md`

---

## 6. 외부 레퍼런스

- https://github.com/openclaw/openclaw — npm 퍼블리시 + `update`/`doctor` 패턴 참고
- https://github.com/666ghj/MiroFish — 멀티 에이전트 시뮬레이션
- https://github.com/anthropics/claude-code — Claude Code CLI 공식
- https://github.com/karpathy/autoresearch — 리서치 자동화 참고
