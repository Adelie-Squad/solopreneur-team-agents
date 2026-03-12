"""
Discord adapter for Solo Founder Agents.
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Callable, Awaitable

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .base import MessengerAdapter, MessageContext

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
REPOS_BASE = Path(os.getenv("REPOS_BASE_PATH", "./repos"))
PRODUCTS_FILE = Path("core/products.json")


def _load_products() -> list[dict]:
    if PRODUCTS_FILE.exists():
        return json.loads(PRODUCTS_FILE.read_text())
    return []


class DiscordMessageContext(MessageContext):
    def __init__(self, message: discord.Message, product: dict, agent_label: str = ""):
        self._message = message
        self._product = product
        self._agent_label = agent_label

    async def reply(self, text: str) -> None:
        chunks = [text[i : i + 1900] for i in range(0, len(text), 1900)]
        for i, chunk in enumerate(chunks):
            prefix = ""
            if i == 0:
                prefix = f"**[{self._product['name']}{self._agent_label}]**\n"
            await self._message.reply(f"{prefix}```\n{chunk}\n```")

    async def typing(self) -> None:
        await self._message.channel.trigger_typing()


class DiscordAdapter(MessengerAdapter):
    """Discord implementation using discord.py."""

    def __init__(self):
        self._bot: commands.Bot | None = None
        self._client: discord.Client | None = None

    @property
    def platform(self) -> str:
        return "discord"

    # ── Bot mode ──

    async def start_bot(
        self,
        on_command: Callable[[str, dict, MessageContext], Awaitable[None]],
    ) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        bot = commands.Bot(command_prefix="!", intents=intents)
        self._bot = bot

        @bot.event
        async def on_ready():
            print(f"[Discord Bot] Logged in: {bot.user}")
            for guild in bot.guilds:
                await self._ensure_channels(guild)
            await self._sync_guild_product_mapping()
            print(f"[Discord Bot] Ready. Connected to {len(bot.guilds)} server(s)")

        @bot.event
        async def on_guild_join(guild: discord.Guild):
            await self._ensure_channels(guild)
            await self._sync_guild_product_mapping()

        @bot.event
        async def on_message(message: discord.Message):
            if message.author.bot:
                return
            if message.channel.name != "owner-command":
                return

            product = self._get_product_by_guild(message.guild.id)
            if not product:
                await message.channel.send(
                    "No product linked to this server. Re-run `setup.py`."
                )
                return

            ctx = DiscordMessageContext(message, product)
            async with message.channel.typing():
                await on_command(message.content.strip(), product, ctx)
            await bot.process_commands(message)

        if not TOKEN:
            print("DISCORD_TOKEN is not set. Check your .env file.")
            raise SystemExit(1)

        await bot.start(TOKEN)

    # ── Notifier mode ──

    async def start_notifier(self) -> None:
        intents = discord.Intents.default()
        self._client = discord.Client(intents=intents)

        if not TOKEN:
            print("DISCORD_TOKEN is not set.")
            raise SystemExit(1)

    async def send_to_channel(
        self,
        product_config: dict,
        channel_name: str,
        text: str,
        title: str | None = None,
    ) -> bool:
        client = self._client or self._bot
        if not client or not client.is_ready():
            return False

        guild_id = product_config.get("guild_id")
        if not guild_id:
            return False

        channel_key = channel_name.replace("-", "_")
        channel_id = product_config.get("channels", {}).get(channel_key)
        if not channel_id:
            return False

        channel = client.get_channel(channel_id)
        if not channel:
            return False

        content = f"**{title}**\n\n{text}" if title else text
        for chunk in [content[i : i + 1900] for i in range(0, len(content), 1900)]:
            await channel.send(chunk)
        return True

    async def setup_channels(self, product_config: dict) -> list[str]:
        client = self._client or self._bot
        if not client:
            return []

        guild_id = product_config.get("guild_id")
        if not guild_id:
            return []

        guild = client.get_guild(guild_id)
        if not guild:
            return []

        return await self._ensure_channels(guild)

    # ── Internal helpers ──

    async def _ensure_channels(self, guild: discord.Guild) -> list[str]:
        existing = {ch.name for ch in guild.channels}

        category = discord.utils.get(guild.categories, name="AI Team Reports")
        if not category:
            category = await guild.create_category("AI Team Reports")

        created = []
        for ch_name in self.channel_names:
            if ch_name not in existing:
                await guild.create_text_channel(ch_name, category=category)
                created.append(ch_name)

        if created:
            print(f"[Discord] {guild.name}: channels created → {', '.join(created)}")
        return created

    async def _sync_guild_product_mapping(self):
        import yaml

        bot = self._bot
        if not bot:
            return

        products = _load_products()
        for guild in bot.guilds:
            for product in products:
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
                            for ch in guild.channels:
                                if ch.name in self.channel_names:
                                    key = ch.name.replace("-", "_")
                                    config["channels"][key] = ch.id
                            config_file.write_text(
                                yaml.dump(config, allow_unicode=True)
                            )
                            print(
                                f"[Discord] Mapped: {guild.name} ↔ {product['name']}"
                            )

    def _get_product_by_guild(self, guild_id: int) -> dict | None:
        import yaml

        products = _load_products()
        for p in products:
            config_file = REPOS_BASE / p["slug"] / "discord" / "config.yaml"
            if config_file.exists():
                config = yaml.safe_load(config_file.read_text())
                if config.get("guild_id") == guild_id:
                    return p
        return None

    def get_client(self) -> discord.Client | None:
        """Return the underlying client (for scheduler to call .run())."""
        return self._client
