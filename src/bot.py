"""
src/bot.py
Discord Bot — 오너의 명령을 받아 Claude Code를 실행하고 결과를 보고
"""

import os
import json
import asyncio
from pathlib import Path
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
REPOS_BASE = Path(os.getenv("REPOS_BASE_PATH", "./repos"))
PRODUCTS_FILE = Path("core/products.json")

CHANNEL_NAMES = [
    "daily-brief",
    "experiments",
    "weekly-review",
    "signals",
    "owner-command",
    "errors",
]

# ──────────────────────────────────────────────
# Bot 초기화
# ──────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


def load_products() -> list[dict]:
    if PRODUCTS_FILE.exists():
        return json.loads(PRODUCTS_FILE.read_text())
    return []


def get_product_by_guild(guild_id: int) -> dict | None:
    """guild_id로 제품 찾기"""
    products = load_products()
    for p in products:
        config_file = REPOS_BASE / p["slug"] / "discord" / "config.yaml"
        if config_file.exists():
            import yaml

            config = yaml.safe_load(config_file.read_text())
            if config.get("guild_id") == guild_id:
                return p
    return None


# ──────────────────────────────────────────────
# 이벤트 핸들러
# ──────────────────────────────────────────────


@bot.event
async def on_ready():
    print(f"[Bot] 로그인: {bot.user}")

    # 각 서버에 채널 자동 생성
    for guild in bot.guilds:
        await ensure_channels(guild)

    # 서버 ↔ 제품 매핑 갱신
    await sync_guild_product_mapping()

    print(f"[Bot] 준비 완료. {len(bot.guilds)}개 서버 연결됨")


@bot.event
async def on_guild_join(guild: discord.Guild):
    """봇이 새 서버에 초대될 때 채널 자동 생성"""
    await ensure_channels(guild)
    await sync_guild_product_mapping()


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # #owner-command 채널에서만 명령 수신
    if message.channel.name != "owner-command":
        return

    product = get_product_by_guild(message.guild.id)
    if not product:
        await message.channel.send(
            "⚠️ 이 서버에 연결된 제품이 없습니다. `setup.py`를 다시 실행하세요."
        )
        return

    await handle_command(message, product)
    await bot.process_commands(message)


# ──────────────────────────────────────────────
# 채널 자동 생성
# ──────────────────────────────────────────────


async def ensure_channels(guild: discord.Guild):
    """필요한 채널이 없으면 자동 생성"""
    existing = {ch.name for ch in guild.channels}

    # 카테고리 생성
    category = discord.utils.get(guild.categories, name="AI 팀 보고")
    if not category:
        category = await guild.create_category("AI 팀 보고")

    created = []
    for ch_name in CHANNEL_NAMES:
        if ch_name not in existing:
            await guild.create_text_channel(ch_name, category=category)
            created.append(ch_name)

    if created:
        print(f"[Bot] {guild.name}: 채널 생성됨 → {', '.join(created)}")


async def sync_guild_product_mapping():
    """서버 이름으로 제품 매핑하고 config.yaml에 guild_id 저장"""
    import yaml

    products = load_products()

    for guild in bot.guilds:
        for product in products:
            # 서버 이름이 제품명을 포함하면 매핑
            if (
                product["name"] in guild.name
                or product["slug"] in guild.name.lower()
            ):
                config_file = (
                    REPOS_BASE / product["slug"] / "discord" / "config.yaml"
                )
                if config_file.exists():
                    config = yaml.safe_load(config_file.read_text())
                    if config.get("guild_id") != guild.id:
                        config["guild_id"] = guild.id
                        # 채널 ID도 저장
                        for ch in guild.channels:
                            if ch.name in CHANNEL_NAMES:
                                key = ch.name.replace("-", "_")
                                config["channels"][key] = ch.id
                        config_file.write_text(
                            yaml.dump(config, allow_unicode=True)
                        )
                        print(
                            f"[Bot] 매핑: {guild.name} ↔ {product['name']}"
                        )


# ──────────────────────────────────────────────
# 명령 처리
# ──────────────────────────────────────────────


async def handle_command(message: discord.Message, product: dict):
    """#owner-command 채널 메시지를 Claude Code로 전달"""

    user_input = message.content.strip()
    product_dir = REPOS_BASE / product["slug"]

    # 타이핑 표시
    async with message.channel.typing():
        result = await run_claude(user_input, product_dir)

    if result:
        # 2000자 초과 시 분할
        chunks = [result[i : i + 1900] for i in range(0, len(result), 1900)]
        for i, chunk in enumerate(chunks):
            prefix = f"**[{product['name']}]**\n" if i == 0 else ""
            await message.reply(f"{prefix}```\n{chunk}\n```")
    else:
        await message.reply("⚠️ 응답을 생성하지 못했습니다.")


async def run_claude(prompt: str, cwd: Path) -> str:
    """Claude Code를 --print 모드로 실행"""
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
        return "⏱️ 응답 시간 초과 (2분). 더 간단한 요청으로 나눠서 시도하세요."
    except FileNotFoundError:
        return "⚠️ Claude Code가 설치되지 않았습니다."
    except Exception as e:
        return f"⚠️ 오류: {str(e)}"


# ──────────────────────────────────────────────
# Discord 보고 유틸 (스케줄러에서 import해서 사용)
# ──────────────────────────────────────────────


async def send_to_channel(
    guild_id: int, channel_name: str, message: str, title: str = None
):
    """특정 서버의 채널에 메시지 전송"""
    guild = bot.get_guild(guild_id)
    if not guild:
        print(f"[Bot] 서버 {guild_id} 를 찾을 수 없음")
        return

    channel = discord.utils.get(guild.channels, name=channel_name)
    if not channel:
        print(f"[Bot] #{channel_name} 채널 없음")
        return

    if title:
        content = f"**{title}**\n{message}"
    else:
        content = message

    # 2000자 제한 처리
    for chunk in [content[i : i + 1900] for i in range(0, len(content), 1900)]:
        await channel.send(chunk)


# ──────────────────────────────────────────────
# 실행
# ──────────────────────────────────────────────

if __name__ == "__main__":
    if not TOKEN:
        print("DISCORD_TOKEN이 설정되지 않았습니다. .env 파일을 확인하세요.")
        exit(1)

    bot.run(TOKEN)
