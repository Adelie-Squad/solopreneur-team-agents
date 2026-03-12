"""
Telegram adapter for Solo Founder Agents.

Uses python-telegram-bot library.
Requires:
  - TELEGRAM_BOT_TOKEN (from @BotFather)
  - TELEGRAM_CHAT_ID (your chat/group ID for receiving commands)
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Callable, Awaitable

from dotenv import load_dotenv

from .base import MessengerAdapter, MessageContext

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
REPOS_BASE = Path(os.getenv("REPOS_BASE_PATH", "./repos"))
PRODUCTS_FILE = Path("core/products.json")

# Telegram message limit
MAX_MESSAGE_LENGTH = 4096


def _load_products() -> list[dict]:
    if PRODUCTS_FILE.exists():
        return json.loads(PRODUCTS_FILE.read_text())
    return []


class TelegramMessageContext(MessageContext):
    def __init__(self, update, context, product: dict, agent_label: str = ""):
        self._update = update
        self._context = context
        self._product = product
        self._agent_label = agent_label

    async def reply(self, text: str) -> None:
        prefix = f"*[{self._product['name']}{self._agent_label}]*\n"
        chunks = [text[i : i + 3800] for i in range(0, len(text), 3800)]
        for i, chunk in enumerate(chunks):
            header = prefix if i == 0 else ""
            await self._update.message.reply_text(
                f"{header}```\n{chunk}\n```",
                parse_mode="Markdown",
            )

    async def typing(self) -> None:
        await self._update.message.chat.send_action(action="typing")


class TelegramAdapter(MessengerAdapter):
    """Telegram implementation using python-telegram-bot."""

    def __init__(self):
        self._app = None
        self._bot = None

    @property
    def platform(self) -> str:
        return "telegram"

    # ── Bot mode ──

    async def start_bot(
        self,
        on_command: Callable[[str, dict, MessageContext], Awaitable[None]],
    ) -> None:
        from telegram.ext import ApplicationBuilder, MessageHandler, filters

        if not TELEGRAM_BOT_TOKEN:
            print("TELEGRAM_BOT_TOKEN is not set. Check .env.")
            raise SystemExit(1)

        self._app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        self._bot = self._app.bot

        async def handle_message(update, context):
            if not update.message or not update.message.text:
                return

            # Only respond to the configured chat
            chat_id = str(update.message.chat.id)
            if TELEGRAM_CHAT_ID and chat_id != TELEGRAM_CHAT_ID:
                return

            # Determine product
            products = _load_products()
            product = self._get_product_for_chat(chat_id)
            if not product:
                product = products[0] if products else None

            if not product:
                await update.message.reply_text(
                    "No product configured. Run `setup.py` first."
                )
                return

            user_text = update.message.text.strip()
            ctx = TelegramMessageContext(update, context, product)
            await ctx.typing()
            await on_command(user_text, product, ctx)

        self._app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        print(f"[Telegram Bot] Starting polling...")
        await self._app.initialize()
        await self._app.start()
        await self._app.updater.start_polling()

        # Keep running
        import asyncio
        stop_event = asyncio.Event()
        await stop_event.wait()

    # ── Notifier mode ──

    async def start_notifier(self) -> None:
        from telegram import Bot

        if not TELEGRAM_BOT_TOKEN:
            print("TELEGRAM_BOT_TOKEN is not set.")
            raise SystemExit(1)

        self._bot = Bot(token=TELEGRAM_BOT_TOKEN)

    async def send_to_channel(
        self,
        product_config: dict,
        channel_name: str,
        text: str,
        title: str | None = None,
    ) -> bool:
        if not self._bot:
            return False

        # Telegram uses chat_id per channel mapping
        channel_key = channel_name.replace("-", "_")
        chat_id = product_config.get("channels", {}).get(channel_key)

        if not chat_id:
            # Fall back to default chat ID
            chat_id = product_config.get("chat_id") or TELEGRAM_CHAT_ID

        if not chat_id:
            return False

        content = f"*{title}*\n\n{text}" if title else text
        try:
            chunks = [content[i : i + 3800] for i in range(0, len(content), 3800)]
            for chunk in chunks:
                await self._bot.send_message(
                    chat_id=chat_id, text=chunk, parse_mode="Markdown"
                )
            return True
        except Exception as e:
            print(f"[Telegram] Failed to send to {chat_id}: {e}")
            return False

    async def setup_channels(self, product_config: dict) -> list[str]:
        # Telegram doesn't support auto-creating channels/groups via bot API.
        # Users must create groups manually and provide chat IDs.
        return []

    # ── Internal helpers ──

    def _get_product_for_chat(self, chat_id: str) -> dict | None:
        import yaml

        products = _load_products()
        for p in products:
            config_file = REPOS_BASE / p["slug"] / "telegram" / "config.yaml"
            if config_file.exists():
                config = yaml.safe_load(config_file.read_text())
                if str(config.get("chat_id")) == chat_id:
                    return p
        return None
