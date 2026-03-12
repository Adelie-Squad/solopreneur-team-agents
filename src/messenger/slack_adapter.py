"""
Slack adapter for Solo Founder Agents.

Uses Slack Bolt for Python (slack_bolt).
Requires:
  - SLACK_BOT_TOKEN (xoxb-...)
  - SLACK_APP_TOKEN (xapp-...) for Socket Mode
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Callable, Awaitable

from dotenv import load_dotenv

from .base import MessengerAdapter, MessageContext

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
REPOS_BASE = Path(os.getenv("REPOS_BASE_PATH", "./repos"))
PRODUCTS_FILE = Path("core/products.json")

# Channel where commands are received
COMMAND_CHANNEL = os.getenv("SLACK_COMMAND_CHANNEL", "owner-command")


def _load_products() -> list[dict]:
    if PRODUCTS_FILE.exists():
        return json.loads(PRODUCTS_FILE.read_text())
    return []


class SlackMessageContext(MessageContext):
    def __init__(self, say_fn, product: dict, agent_label: str = ""):
        self._say = say_fn
        self._product = product
        self._agent_label = agent_label

    async def reply(self, text: str) -> None:
        prefix = f"*[{self._product['name']}{self._agent_label}]*\n"
        # Slack message limit is ~40k chars, but keep chunks reasonable
        chunks = [text[i : i + 3000] for i in range(0, len(text), 3000)]
        for i, chunk in enumerate(chunks):
            header = prefix if i == 0 else ""
            await self._say(f"{header}```\n{chunk}\n```")

    async def typing(self) -> None:
        pass  # Slack shows typing automatically for bot responses


class SlackAdapter(MessengerAdapter):
    """Slack implementation using slack_bolt (Socket Mode)."""

    def __init__(self):
        self._app = None
        self._client = None

    @property
    def platform(self) -> str:
        return "slack"

    # ── Bot mode ──

    async def start_bot(
        self,
        on_command: Callable[[str, dict, MessageContext], Awaitable[None]],
    ) -> None:
        from slack_bolt.async_app import AsyncApp
        from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

        self._app = AsyncApp(token=SLACK_BOT_TOKEN)
        self._client = self._app.client

        @self._app.message("")
        async def handle_message(message, say):
            # Only respond in the command channel
            channel_info = await self._client.conversations_info(
                channel=message["channel"]
            )
            channel_name = channel_info["channel"]["name"]

            if channel_name != COMMAND_CHANNEL:
                return

            # Determine product from workspace or channel metadata
            product = self._get_product_for_channel(message["channel"])
            if not product:
                products = _load_products()
                product = products[0] if products else None

            if not product:
                await say("No product configured. Run `setup.py` first.")
                return

            user_text = message.get("text", "").strip()
            ctx = SlackMessageContext(say, product)
            await on_command(user_text, product, ctx)

        if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
            print("SLACK_BOT_TOKEN and SLACK_APP_TOKEN are required. Check .env.")
            raise SystemExit(1)

        handler = AsyncSocketModeHandler(self._app, SLACK_APP_TOKEN)
        print("[Slack Bot] Starting Socket Mode...")
        await handler.start_async()

    # ── Notifier mode ──

    async def start_notifier(self) -> None:
        from slack_sdk.web.async_client import AsyncWebClient

        if not SLACK_BOT_TOKEN:
            print("SLACK_BOT_TOKEN is not set.")
            raise SystemExit(1)

        self._client = AsyncWebClient(token=SLACK_BOT_TOKEN)

    async def send_to_channel(
        self,
        product_config: dict,
        channel_name: str,
        text: str,
        title: str | None = None,
    ) -> bool:
        if not self._client:
            return False

        channel_key = channel_name.replace("-", "_")
        channel_id = product_config.get("channels", {}).get(channel_key)

        if not channel_id:
            # Try to find channel by name
            channel_id = await self._find_channel_by_name(channel_name)
            if not channel_id:
                return False

        content = f"*{title}*\n\n{text}" if title else text
        try:
            await self._client.chat_postMessage(channel=channel_id, text=content)
            return True
        except Exception as e:
            print(f"[Slack] Failed to send to #{channel_name}: {e}")
            return False

    async def setup_channels(self, product_config: dict) -> list[str]:
        if not self._client:
            return []

        existing = await self._list_channels()
        existing_names = {ch["name"] for ch in existing}

        created = []
        for ch_name in self.channel_names:
            if ch_name not in existing_names:
                try:
                    await self._client.conversations_create(name=ch_name)
                    created.append(ch_name)
                except Exception as e:
                    print(f"[Slack] Failed to create #{ch_name}: {e}")

        if created:
            print(f"[Slack] Channels created: {', '.join(created)}")
        return created

    # ── Internal helpers ──

    async def _list_channels(self) -> list[dict]:
        try:
            result = await self._client.conversations_list(
                types="public_channel,private_channel", limit=1000
            )
            return result.get("channels", [])
        except Exception:
            return []

    async def _find_channel_by_name(self, name: str) -> str | None:
        channels = await self._list_channels()
        for ch in channels:
            if ch["name"] == name:
                return ch["id"]
        return None

    def _get_product_for_channel(self, channel_id: str) -> dict | None:
        """Try to match channel to product via config."""
        import yaml

        products = _load_products()
        for p in products:
            config_file = REPOS_BASE / p["slug"] / "slack" / "config.yaml"
            if config_file.exists():
                config = yaml.safe_load(config_file.read_text())
                channels = config.get("channels", {})
                if channel_id in channels.values():
                    return p
        return None
