"""
src/scheduler.py
Automated routine execution + messenger reporting + memory auto-save.
Supports: Discord, Slack, Telegram (configured via MESSENGER env var)
"""

import os
import re
import json
import asyncio
from pathlib import Path
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

load_dotenv()

REPOS_BASE = Path(os.getenv("REPOS_BASE_PATH", "./repos"))
ROUTINES_DIR = Path("routines")
PRODUCTS_FILE = Path("core/products.json")

# ──────────────────────────────────────────────
# Routine definitions
# ──────────────────────────────────────────────

ROUTINES = [
    {
        "id": "morning-brief",
        "name": "Morning Brief",
        "schedule": {"hour": 6, "minute": 0},
        "channel": "daily-brief",
        "emoji": "📋",
        "memory_targets": [],
    },
    {
        "id": "signal-scan",
        "name": "Signal Scan",
        "schedule": {"hour": 12, "minute": 0},
        "channel": "signals",
        "emoji": "🔍",
        "memory_targets": ["signals.jsonl"],
    },
    {
        "id": "experiment-check",
        "name": "Experiment Check",
        "schedule": {"hour": 16, "minute": 0},
        "channel": "experiments",
        "emoji": "🧪",
        "memory_targets": ["experiments.jsonl"],
    },
    {
        "id": "daily-log",
        "name": "Daily Log",
        "schedule": {"hour": 22, "minute": 0},
        "channel": "daily-brief",
        "emoji": "📝",
        "memory_targets": ["decisions.jsonl"],
    },
    {
        "id": "weekly-review",
        "name": "Weekly Review",
        "schedule": {"day_of_week": "sun", "hour": 20, "minute": 0},
        "channel": "weekly-review",
        "emoji": "📊",
        "memory_targets": ["decisions.jsonl"],
    },
]

# ──────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────


def load_products() -> list[dict]:
    if PRODUCTS_FILE.exists():
        return json.loads(PRODUCTS_FILE.read_text())
    return []


def load_messenger_config(product_slug: str) -> dict:
    """Load product's messenger config (discord/slack/telegram)."""
    import yaml

    messenger = os.getenv("MESSENGER", "discord").lower()
    config_file = REPOS_BASE / product_slug / messenger / "config.yaml"
    if config_file.exists():
        return yaml.safe_load(config_file.read_text()) or {}
    return {}


def load_routine_prompt(routine_id: str) -> str:
    prompt_file = ROUTINES_DIR / f"{routine_id}.md"
    if prompt_file.exists():
        return prompt_file.read_text()
    return f"# {routine_id}\n\nPrompt file missing: routines/{routine_id}.md"


async def run_claude_async(prompt: str, cwd: Path) -> str:
    """Run Claude Code --print asynchronously."""
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
        return result if result else "No response"
    except asyncio.TimeoutError:
        return "⏱️ Timeout (exceeded 3 min)"
    except Exception as e:
        return f"⚠️ Error: {e}"


def extract_json_blocks(text: str) -> list[dict]:
    """Extract JSON blocks from routine results."""
    items = []
    for match in re.finditer(r"```json\s*\n(.*?)\n\s*```", text, re.DOTALL):
        raw = match.group(1).strip()
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict) and not obj.get("_schema"):
                    items.append(obj)
            except json.JSONDecodeError:
                pass
    return items


def append_to_jsonl(file_path: Path, items: list[dict]):
    """Append items to JSONL file (with dedup)."""
    if not items:
        return 0

    existing = set()
    if file_path.exists():
        for line in file_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('{"_schema'):
                existing.add(line)

    added = 0
    with open(file_path, "a") as f:
        for item in items:
            if "date" not in item:
                item["date"] = datetime.now().strftime("%Y-%m-%d")
            line = json.dumps(item, ensure_ascii=False)
            if line not in existing:
                f.write(line + "\n")
                added += 1
    return added


def save_routine_memory(result: str, routine: dict, product_dir: Path):
    """Extract JSON from routine result and append to JSONL memory."""
    targets = routine.get("memory_targets", [])
    if not targets:
        return

    items = extract_json_blocks(result)
    if not items:
        return

    memory_dir = product_dir / "memory"
    total = 0
    for target in targets:
        target_path = memory_dir / target
        if target_path.exists():
            added = append_to_jsonl(target_path, items)
            total += added

    if total > 0:
        print(f"[Scheduler] Memory saved: {total} item(s) → {', '.join(targets)}")


# ──────────────────────────────────────────────
# Messenger adapter (initialized at startup)
# ──────────────────────────────────────────────

adapter = None


# ──────────────────────────────────────────────
# Routine execution
# ──────────────────────────────────────────────


async def run_routine_for_product(routine: dict, product: dict):
    """Execute a routine for a single product."""
    product_slug = product["slug"]
    product_name = product["name"]
    product_dir = REPOS_BASE / product_slug

    print(f"[Scheduler] {product_name} - {routine['name']} starting")

    prompt = load_routine_prompt(routine["id"])
    result = await run_claude_async(prompt, product_dir)

    # Auto-save to memory
    save_routine_memory(result, routine, product_dir)

    # Always save routine log to file
    log_dir = product_dir / "memory" / "routine-logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / (
        f"{routine['id']}-{datetime.now().strftime('%Y%m%d-%H%M')}.md"
    )
    log_file.write_text(f"# {routine['name']}\n\n{result}")

    # Send to messenger
    if adapter:
        config = load_messenger_config(product_slug)
        title = (
            f"{routine['emoji']} [{routine['name']}] {product_name}"
            f" | {datetime.now().strftime('%m-%d %H:%M')}"
        )
        sent = await adapter.send_to_channel(
            config, routine["channel"], result, title
        )
        if sent:
            print(
                f"[Scheduler] {product_name} - {routine['name']}"
                f" → {adapter.platform} sent"
            )
        else:
            print(
                f"[Scheduler] {product_name}"
                f" - No {adapter.platform} config. Saved to file only."
            )


async def run_routine(routine_id: str):
    """Run a routine for all products in parallel."""
    routine = next((r for r in ROUTINES if r["id"] == routine_id), None)
    if not routine:
        print(f"[Scheduler] Unknown routine: {routine_id}")
        return

    products = load_products()
    if not products:
        print("[Scheduler] No products registered")
        return

    tasks = [run_routine_for_product(routine, p) for p in products]
    await asyncio.gather(*tasks, return_exceptions=True)


# ──────────────────────────────────────────────
# Scheduler setup
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
        print(f"[Scheduler] Registered: {routine['name']} ({schedule})")


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────


async def main():
    global adapter

    from messenger import create_adapter

    adapter = create_adapter()
    print(f"[Scheduler] Using {adapter.platform} adapter")

    messenger = os.getenv("MESSENGER", "discord").lower()

    if messenger == "discord":
        # Discord needs a client connection to send messages
        import discord

        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f"[Scheduler] {adapter.platform} connected: {client.user}")

            if not scheduler.running:
                setup_schedules()
                scheduler.start()
                print("[Scheduler] Scheduler started")

            # Startup notification
            products = load_products()
            for product in products:
                config = load_messenger_config(product["slug"])
                await adapter.send_to_channel(
                    config,
                    "daily-brief",
                    "**AI Assistant System Started**\n"
                    "Routine schedule:\n"
                    + "\n".join(
                        f"• {r['emoji']} {r['name']}: {r['schedule']}"
                        for r in ROUTINES
                    ),
                )

        # Inject client into discord adapter
        adapter._client = client
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("DISCORD_TOKEN is not set")
            return
        await client.start(token)

    else:
        # Slack and Telegram: use adapter's notifier mode
        await adapter.start_notifier()

        setup_schedules()
        scheduler.start()
        print("[Scheduler] Scheduler started")

        # Startup notification
        products = load_products()
        for product in products:
            config = load_messenger_config(product["slug"])
            await adapter.send_to_channel(
                config,
                "daily-brief",
                "**AI Assistant System Started**\n"
                "Routine schedule:\n"
                + "\n".join(
                    f"• {r['emoji']} {r['name']}: {r['schedule']}"
                    for r in ROUTINES
                ),
            )

        # Keep running
        stop_event = asyncio.Event()
        await stop_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
