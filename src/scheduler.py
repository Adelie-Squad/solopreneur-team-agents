"""
src/scheduler.py
24시간 루틴 자동 실행 + Discord 보고
"""

import os
import json
import asyncio
from pathlib import Path
from datetime import datetime

import discord
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
REPOS_BASE = Path(os.getenv("REPOS_BASE_PATH", "./repos"))
ROUTINES_DIR = Path("routines")
PRODUCTS_FILE = Path("core/products.json")

# ──────────────────────────────────────────────
# 루틴 정의
# schedule: APScheduler cron 표현식
# channel: 보고할 Discord 채널명
# ──────────────────────────────────────────────

ROUTINES = [
    {
        "id": "morning-brief",
        "name": "Morning Brief",
        "schedule": {"hour": 6, "minute": 0},
        "channel": "daily-brief",
        "emoji": "📋",
    },
    {
        "id": "signal-scan",
        "name": "Signal Scan",
        "schedule": {"hour": 12, "minute": 0},
        "channel": "signals",
        "emoji": "🔍",
    },
    {
        "id": "experiment-check",
        "name": "Experiment Check",
        "schedule": {"hour": 16, "minute": 0},
        "channel": "experiments",
        "emoji": "🧪",
    },
    {
        "id": "daily-log",
        "name": "Daily Log",
        "schedule": {"hour": 22, "minute": 0},
        "channel": "daily-brief",
        "emoji": "📝",
    },
    {
        "id": "weekly-review",
        "name": "Weekly Review",
        "schedule": {"day_of_week": "sun", "hour": 20, "minute": 0},
        "channel": "weekly-review",
        "emoji": "📊",
    },
]

# ──────────────────────────────────────────────
# 유틸
# ──────────────────────────────────────────────


def load_products() -> list[dict]:
    if PRODUCTS_FILE.exists():
        return json.loads(PRODUCTS_FILE.read_text())
    return []


def load_discord_config(product_slug: str) -> dict:
    import yaml

    config_file = REPOS_BASE / product_slug / "discord" / "config.yaml"
    if config_file.exists():
        return yaml.safe_load(config_file.read_text()) or {}
    return {}


def load_routine_prompt(routine_id: str) -> str:
    prompt_file = ROUTINES_DIR / f"{routine_id}.md"
    if prompt_file.exists():
        return prompt_file.read_text()
    return f"# {routine_id} 루틴\n\n프롬프트 파일이 없습니다: routines/{routine_id}.md"


async def run_claude_async(prompt: str, cwd: Path) -> str:
    """Claude Code --print 비동기 실행"""
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
            timeout=180,
        )
        result = stdout.decode().strip()
        return result if result else "응답 없음"
    except asyncio.TimeoutError:
        return "⏱️ 타임아웃 (3분 초과)"
    except Exception as e:
        return f"⚠️ 오류: {e}"


def send_discord_webhook(webhook_url: str, content: str, title: str = ""):
    """웹훅으로 Discord 메시지 전송 (봇 없이도 가능한 폴백)"""
    payload = {"content": f"**{title}**\n{content}" if title else content}
    try:
        requests.post(webhook_url, json=payload, timeout=10)
    except Exception as e:
        print(f"[Scheduler] 웹훅 전송 실패: {e}")


# ──────────────────────────────────────────────
# 루틴 실행
# ──────────────────────────────────────────────

# Discord 봇 클라이언트 (채널 ID로 직접 전송)
intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def run_routine_for_product(routine: dict, product: dict):
    """단일 제품에 대해 루틴 실행"""
    product_slug = product["slug"]
    product_name = product["name"]
    product_dir = REPOS_BASE / product_slug

    print(f"[Scheduler] {product_name} - {routine['name']} 시작")

    # 프롬프트 로드
    prompt = load_routine_prompt(routine["id"])

    # Claude Code 실행
    result = await run_claude_async(prompt, product_dir)

    # Discord 보고
    config = load_discord_config(product_slug)
    guild_id = config.get("guild_id")

    if guild_id and client.is_ready():
        channel_name = routine["channel"]
        channel_key = channel_name.replace("-", "_")
        channel_id = config.get("channels", {}).get(channel_key)

        if channel_id:
            channel = client.get_channel(channel_id)
            if channel:
                title = (
                    f"{routine['emoji']} [{routine['name']}] {product_name}"
                    f" | {datetime.now().strftime('%m-%d %H:%M')}"
                )

                # 2000자 제한
                message = f"**{title}**\n\n{result}"
                chunks = [
                    message[i : i + 1900]
                    for i in range(0, len(message), 1900)
                ]
                for chunk in chunks:
                    await channel.send(chunk)
                print(
                    f"[Scheduler] {product_name} - {routine['name']}"
                    " → Discord 전송 완료"
                )
                return

    # 웹훅 폴백
    webhook_url = config.get("webhook_url")
    if webhook_url:
        title = f"{routine['emoji']} [{routine['name']}] {product_name}"
        send_discord_webhook(webhook_url, result, title)
    else:
        print(
            f"[Scheduler] {product_name}"
            " - Discord 설정 없음. 결과를 파일에 저장."
        )
        log_dir = product_dir / "memory" / "routine-logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / (
            f"{routine['id']}-{datetime.now().strftime('%Y%m%d-%H%M')}.md"
        )
        log_file.write_text(f"# {routine['name']}\n\n{result}")


async def run_routine(routine_id: str):
    """모든 제품에 대해 루틴 병렬 실행"""
    routine = next((r for r in ROUTINES if r["id"] == routine_id), None)
    if not routine:
        print(f"[Scheduler] 알 수 없는 루틴: {routine_id}")
        return

    products = load_products()
    if not products:
        print("[Scheduler] 등록된 제품 없음")
        return

    # 모든 제품 병렬 실행
    tasks = [run_routine_for_product(routine, p) for p in products]
    await asyncio.gather(*tasks, return_exceptions=True)


# ──────────────────────────────────────────────
# 스케줄러 설정
# ──────────────────────────────────────────────

scheduler = AsyncIOScheduler(timezone="Asia/Seoul")


def setup_schedules():
    for routine in ROUTINES:
        schedule = routine["schedule"]

        trigger = CronTrigger(timezone="Asia/Seoul", **schedule)

        scheduler.add_job(
            run_routine,
            trigger=trigger,
            args=[routine["id"]],
            id=routine["id"],
            replace_existing=True,
        )
        print(f"[Scheduler] 등록: {routine['name']} ({schedule})")


# ──────────────────────────────────────────────
# Discord 클라이언트 이벤트
# ──────────────────────────────────────────────


@client.event
async def on_ready():
    print(f"[Scheduler] Discord 연결됨: {client.user}")

    if not scheduler.running:
        setup_schedules()
        scheduler.start()
        print("[Scheduler] 스케줄러 시작됨")

    # 시작 알림 (모든 제품 daily-brief 채널)
    products = load_products()
    for product in products:
        config = load_discord_config(product["slug"])
        channel_id = config.get("channels", {}).get("daily_brief")
        if channel_id:
            channel = client.get_channel(channel_id)
            if channel:
                await channel.send(
                    f"**solopreneur-agents 시작됨**\n"
                    f"다음 루틴 스케줄:\n"
                    + "\n".join(
                        f"• {r['emoji']} {r['name']}: {r['schedule']}"
                        for r in ROUTINES
                    )
                )


# ──────────────────────────────────────────────
# 실행
# ──────────────────────────────────────────────

if __name__ == "__main__":
    if not TOKEN:
        print("DISCORD_TOKEN 없음")
        exit(1)

    client.run(TOKEN)
