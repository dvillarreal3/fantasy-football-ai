"""Discord delivery helpers for fantasy reports."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Optional


class DiscordNotifierError(RuntimeError):
    """Raised when Discord delivery cannot be completed."""


@dataclass
class DiscordNotifier:
    """Send recommendation reports to a configured Discord channel."""

    bot_token: Optional[str] = None
    channel_id: Optional[int] = None

    def send_lineup_report(self, report: dict[str, Any]) -> str:
        """Format and send a lineup report."""
        message = self._format_report("Lineup Report", report)
        self._send_if_configured(message)
        return message

    def send_trade_report(self, report: dict[str, Any]) -> str:
        """Format and send a trade report."""
        message = self._format_report("Trade Report", report)
        self._send_if_configured(message)
        return message

    def send_pickup_report(self, report: dict[str, Any]) -> str:
        """Format and send a pickup report."""
        message = self._format_report("Pickup Report", report)
        self._send_if_configured(message)
        return message

    def _send_if_configured(self, message: str) -> None:
        """Attempt to send a message to Discord when credentials are configured."""
        if not self.bot_token or not self.channel_id:
            return

        asyncio.run(self._send_message(message))

    async def _send_message(self, message: str) -> None:
        """Open a short-lived Discord client to send one message."""
        try:
            import discord
        except ImportError as exc:
            raise DiscordNotifierError("The `discord.py` package is required for Discord delivery.") from exc

        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready() -> None:  # pragma: no cover - external service dependency
            channel = client.get_channel(self.channel_id)
            if channel is None:
                await client.close()
                raise DiscordNotifierError("Discord channel could not be found.")

            await channel.send(message)
            await client.close()

        try:
            await client.start(self.bot_token)
        except Exception as exc:  # pragma: no cover - external service dependency
            raise DiscordNotifierError(f"Failed to send Discord message: {exc}") from exc

    @staticmethod
    def _format_report(title: str, report: dict[str, Any]) -> str:
        """Return a markdown-friendly Discord message."""
        summary = report.get("analysis", {}).get("summary", "No AI summary available.")
        return f"**{title}**\nTeam: {report.get('team_name', 'Unknown')}\n\n{summary}"
