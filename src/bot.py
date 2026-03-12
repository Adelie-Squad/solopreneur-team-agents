"""
src/bot.py
Messenger Bot — Receives owner commands, routes to agents, executes via Claude Code.
Supports: Discord, Slack, Telegram (configured via MESSENGER env var)
"""

import os
import asyncio
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

REPOS_BASE = Path(os.getenv("REPOS_BASE_PATH", "./repos"))
AGENTS_DIR = Path("agents")

# ──────────────────────────────────────────────
# Agent routing
# ──────────────────────────────────────────────

AGENT_ROUTES = {
    # Strategy
    "pmf": ("strategy", "pmf-planner"),
    "시장 적합": ("strategy", "pmf-planner"),
    "가설": ("strategy", "pmf-planner"),
    "기능 기획": ("strategy", "feature-planner"),
    "기능 추가": ("strategy", "feature-planner"),
    "스펙": ("strategy", "feature-planner"),
    "정책": ("strategy", "policy-architect"),
    "약관": ("strategy", "policy-architect"),
    "데이터 분석": ("strategy", "data-analyst"),
    "지표": ("strategy", "data-analyst"),
    "매출": ("strategy", "data-analyst"),
    "사업 전략": ("strategy", "business-strategist"),
    "수익 모델": ("strategy", "business-strategist"),
    "비즈니스": ("strategy", "business-strategist"),
    "아이디어": ("strategy", "idea-refiner"),
    "브레인스토밍": ("strategy", "idea-refiner"),
    "일정": ("strategy", "scope-estimator"),
    "견적": ("strategy", "scope-estimator"),
    "스코프": ("strategy", "scope-estimator"),
    # Growth
    "마케팅": ("growth", "gtm-strategist"),
    "gtm": ("growth", "gtm-strategist"),
    "런칭": ("growth", "gtm-strategist"),
    "카피": ("growth", "content-writer"),
    "블로그": ("growth", "content-writer"),
    "글쓰기": ("growth", "content-writer"),
    "콘텐츠": ("growth", "content-writer"),
    "브랜드": ("growth", "brand-marketer"),
    "브랜딩": ("growth", "brand-marketer"),
    "네이밍": ("growth", "brand-marketer"),
    "광고": ("growth", "paid-marketer"),
    "퍼포먼스": ("growth", "paid-marketer"),
    "cpa": ("growth", "paid-marketer"),
    # Experience
    "유저 리서치": ("experience", "user-researcher"),
    "인터뷰": ("experience", "user-researcher"),
    "설문": ("experience", "user-researcher"),
    "페르소나": ("experience", "user-researcher"),
    "시장 조사": ("experience", "desk-researcher"),
    "경쟁사": ("experience", "desk-researcher"),
    "벤치마크": ("experience", "desk-researcher"),
    "ux": ("experience", "ux-designer"),
    "와이어프레임": ("experience", "ux-designer"),
    "사용성": ("experience", "ux-designer"),
    "플로우": ("experience", "ux-designer"),
    "ui": ("experience", "ui-designer"),
    "디자인 시스템": ("experience", "ui-designer"),
    "목업": ("experience", "ui-designer"),
    # Engineering
    "프론트": ("engineering", "creative-frontend"),
    "프론트엔드": ("engineering", "creative-frontend"),
    "랜딩": ("engineering", "creative-frontend"),
    "프로토타입": ("engineering", "fde"),
    "mvp": ("engineering", "fde"),
    "빠르게 만들": ("engineering", "fde"),
    "아키텍처": ("engineering", "architect"),
    "설계": ("engineering", "architect"),
    "시스템 구조": ("engineering", "architect"),
    "백엔드": ("engineering", "backend-developer"),
    "서버": ("engineering", "backend-developer"),
    "db": ("engineering", "backend-developer"),
    "api": ("engineering", "api-developer"),
    "엔드포인트": ("engineering", "api-developer"),
    "크롤링": ("engineering", "data-collector"),
    "수집": ("engineering", "data-collector"),
    "스크래핑": ("engineering", "data-collector"),
    "파이프라인": ("engineering", "data-engineer"),
    "etl": ("engineering", "data-engineer"),
    "배포": ("engineering", "cloud-admin"),
    "인프라": ("engineering", "cloud-admin"),
    "도커": ("engineering", "cloud-admin"),
    "ci/cd": ("engineering", "cloud-admin"),
}


def find_agent(user_input: str) -> tuple[str, str] | None:
    """Find the best matching agent for user input."""
    lower = user_input.lower()
    for keyword, (team, agent) in AGENT_ROUTES.items():
        if keyword in lower:
            return team, agent
    return None


def load_agent_skill(team: str, agent: str) -> str:
    """Load agent SKILL.md."""
    skill_file = AGENTS_DIR / team / agent / "SKILL.md"
    if skill_file.exists():
        return skill_file.read_text()
    return ""


# ──────────────────────────────────────────────
# Claude Code execution
# ──────────────────────────────────────────────


async def run_claude(prompt: str, cwd: Path) -> str:
    """Run Claude Code in --print mode."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "claude",
            "--print",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(cwd),
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(input=prompt.encode()),
            timeout=120,
        )
        return stdout.decode().strip()
    except asyncio.TimeoutError:
        return "Response timed out (2 min). Try splitting into simpler requests."
    except FileNotFoundError:
        return "Claude Code is not installed. Check the `claude` command."
    except Exception as e:
        return f"Error: {str(e)}"


# ──────────────────────────────────────────────
# Command handler (platform-agnostic)
# ──────────────────────────────────────────────


async def handle_command(user_input: str, product: dict, ctx) -> None:
    """Route user input to agent and respond via messenger context."""
    product_dir = REPOS_BASE / product["slug"]

    # Agent routing
    route = find_agent(user_input)
    skill_context = ""

    if route:
        team, agent = route
        skill = load_agent_skill(team, agent)
        if skill:
            skill_context = (
                f"\n\n--- Agent Skill ---\n{skill}\n--- End Skill ---\n\n"
            )
            ctx._agent_label = f" ({agent})"
            print(f"[Bot] Routing: {user_input[:50]}... → {team}/{agent}")

    prompt = f"{skill_context}{user_input}" if skill_context else user_input

    result = await run_claude(prompt, product_dir)

    if result:
        await ctx.reply(result)
    else:
        await ctx.reply("Failed to generate a response.")


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    from messenger import create_adapter

    adapter = create_adapter()
    print(f"[Bot] Starting with {adapter.platform} adapter...")

    asyncio.run(adapter.start_bot(handle_command))
