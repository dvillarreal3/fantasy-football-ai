"""Core package exports for the Fantasy Football AI assistant."""

from __future__ import annotations

from typing import Optional

from fantasy_ai.ai_analyzer import AIAnalyzer
from fantasy_ai.data_enrichment import DataEnrichment
from fantasy_ai.discord_notifier import DiscordNotifier
from fantasy_ai.espn_connector import ESPNConnector
from fantasy_ai.recommendations import RecommendationEngine

__all__ = [
    "AIAnalyzer",
    "DataEnrichment",
    "DiscordNotifier",
    "ESPNConnector",
    "FantasyAssistant",
    "RecommendationEngine",
]

__version__ = "0.1.0"


class FantasyAssistant:
    """High-level facade that coordinates the core assistant modules."""

    def __init__(
        self,
        league_id: int | str,
        ai_provider: str = "claude",
        *,
        espn_s2: Optional[str] = None,
        swid: Optional[str] = None,
        ai_api_key: Optional[str] = None,
        discord_token: Optional[str] = None,
        discord_channel_id: Optional[int] = None,
    ) -> None:
        """Initialize the assistant with the default production components."""
        self.connector = ESPNConnector(league_id=league_id, espn_s2=espn_s2, swid=swid)
        self.analyzer = AIAnalyzer(provider=ai_provider, api_key=ai_api_key)
        self.enrichment = DataEnrichment()
        self.recommendations = RecommendationEngine(
            connector=self.connector,
            analyzer=self.analyzer,
            enrichment=self.enrichment,
        )
        self.notifier = DiscordNotifier(
            bot_token=discord_token,
            channel_id=discord_channel_id,
        )

    def get_lineup_recommendations(self, team_id: Optional[int] = None) -> dict:
        """Return lineup advice for the configured league."""
        return self.recommendations.get_lineup_recommendations(team_id=team_id)

    def analyze_trade_opportunities(self, team_id: Optional[int] = None) -> dict:
        """Return trade opportunities for the configured league."""
        return self.recommendations.analyze_trade_opportunities(team_id=team_id)

    def get_pickup_suggestions(self, team_id: Optional[int] = None, limit: int = 5) -> dict:
        """Return waiver wire pickup suggestions for the configured league."""
        return self.recommendations.get_pickup_suggestions(team_id=team_id, limit=limit)
