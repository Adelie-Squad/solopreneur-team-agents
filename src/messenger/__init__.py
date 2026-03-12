"""
Messenger adapter factory.

Supports: discord, slack, telegram
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import MessengerAdapter


def create_adapter(platform: str | None = None) -> "MessengerAdapter":
    """Create a messenger adapter based on platform name or MESSENGER env var."""
    platform = (platform or os.getenv("MESSENGER", "discord")).lower()

    if platform == "discord":
        from .discord_adapter import DiscordAdapter
        return DiscordAdapter()
    elif platform == "slack":
        from .slack_adapter import SlackAdapter
        return SlackAdapter()
    elif platform == "telegram":
        from .telegram_adapter import TelegramAdapter
        return TelegramAdapter()
    else:
        raise ValueError(f"Unsupported messenger platform: {platform}")
