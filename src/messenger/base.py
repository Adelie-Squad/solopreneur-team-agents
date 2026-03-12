"""
Abstract base class for messenger adapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Awaitable


class MessengerAdapter(ABC):
    """
    Unified interface for messenger platforms (Discord, Slack, Telegram).

    Two modes:
      - Bot mode: listens for commands and responds (src/bot.py)
      - Notifier mode: sends scheduled reports to channels (src/scheduler.py)
    """

    # ── Bot mode ──

    @abstractmethod
    async def start_bot(
        self,
        on_command: Callable[[str, dict, "MessageContext"], Awaitable[None]],
    ) -> None:
        """
        Start listening for messages.

        Args:
            on_command: callback(user_text, product_dict, ctx)
                        The bot calls this when a message arrives in the
                        command channel. The callback should call ctx.reply()
                        when done.
        """

    # ── Notifier mode ──

    @abstractmethod
    async def start_notifier(self) -> None:
        """Start the notifier client (connect but don't listen for commands)."""

    @abstractmethod
    async def send_to_channel(
        self,
        product_config: dict,
        channel_name: str,
        text: str,
        title: str | None = None,
    ) -> bool:
        """
        Send a message to a named channel for a product.

        Args:
            product_config: product's messenger config (loaded from config.yaml)
            channel_name: logical channel name (e.g. "daily-brief", "signals")
            text: message body
            title: optional bold title prefix

        Returns:
            True if sent successfully
        """

    # ── Setup ──

    @abstractmethod
    async def setup_channels(self, product_config: dict) -> list[str]:
        """
        Ensure required channels exist for a product.
        Returns list of newly created channel names.
        """

    # ── Shared ──

    @property
    @abstractmethod
    def platform(self) -> str:
        """Platform name: 'discord', 'slack', or 'telegram'."""

    @property
    def channel_names(self) -> list[str]:
        """Logical channel names this system uses."""
        return [
            "daily-brief",
            "experiments",
            "weekly-review",
            "signals",
            "owner-command",
            "errors",
        ]


class MessageContext:
    """
    Platform-agnostic message context passed to on_command callback.
    Adapters subclass this to wrap platform-specific reply logic.
    """

    @abstractmethod
    async def reply(self, text: str) -> None:
        """Reply to the original message."""

    @abstractmethod
    async def typing(self) -> None:
        """Show typing indicator."""
