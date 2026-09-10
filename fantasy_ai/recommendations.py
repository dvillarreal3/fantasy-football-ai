"""Recommendation engine for lineup, trade, and pickup advice."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from utils.helpers import build_optimal_lineup, group_players_by_position, sort_players_by_projection


class ConnectorProtocol(Protocol):
    """Protocol for the subset of connector behavior used by recommendations."""

    def get_my_team(self, team_id: int | None = None) -> dict[str, Any]:
        """Return team information."""

    def get_waiver_wire(self, limit: int = 25) -> list[dict[str, Any]]:
        """Return available free agents."""


class AnalyzerProtocol(Protocol):
    """Protocol for the subset of analyzer behavior used by recommendations."""

    def analyze_lineup(self, lineup_context: dict[str, Any]) -> dict[str, Any]:
        """Analyze lineup decisions."""

    def evaluate_trades(self, trade_context: dict[str, Any]) -> dict[str, Any]:
        """Analyze trade decisions."""

    def suggest_pickups(self, waiver_context: dict[str, Any]) -> dict[str, Any]:
        """Analyze waiver wire pickups."""


class EnrichmentProtocol(Protocol):
    """Protocol for supplemental enrichment behavior."""

    def get_player_news(self, player_name: str) -> list[dict[str, Any]]:
        """Return recent player news."""

    def get_injury_reports(self, player_name: str | None = None) -> list[dict[str, Any]]:
        """Return injury reports."""

    def get_expert_rankings(self, players: list[str]) -> list[dict[str, Any]]:
        """Return expert rankings."""


@dataclass
class RecommendationEngine:
    """Generate deterministic recommendations with optional AI summaries."""

    connector: ConnectorProtocol
    analyzer: AnalyzerProtocol
    enrichment: EnrichmentProtocol

    def get_lineup_recommendations(self, team_id: int | None = None) -> dict[str, Any]:
        """Return lineup recommendations for the given team."""
        team = self.connector.get_my_team(team_id=team_id)
        roster = sort_players_by_projection(team.get("roster", []))
        starters, bench = build_optimal_lineup(roster)
        injuries = self.enrichment.get_injury_reports()

        context = {
            "team_name": team.get("team_name"),
            "starters": starters,
            "bench": bench,
            "injuries": injuries,
        }
        analysis = self.analyzer.analyze_lineup(context)
        return {
            "team_name": team.get("team_name"),
            "recommended_starters": starters,
            "bench_candidates": bench,
            "analysis": analysis,
        }

    def analyze_trade_opportunities(self, team_id: int | None = None) -> dict[str, Any]:
        """Return a simple trade recommendation payload."""
        team = self.connector.get_my_team(team_id=team_id)
        grouped = group_players_by_position(team.get("roster", []))
        strengths = [position for position, players in grouped.items() if len(players) >= 3]
        needs = [position for position, players in grouped.items() if len(players) <= 1]

        context = {
            "team_name": team.get("team_name"),
            "strength_positions": strengths,
            "need_positions": needs,
            "roster_snapshot": grouped,
        }
        analysis = self.analyzer.evaluate_trades(context)
        return {
            "team_name": team.get("team_name"),
            "trade_targets": needs,
            "trade_chips": strengths,
            "analysis": analysis,
        }

    def get_pickup_suggestions(self, team_id: int | None = None, limit: int = 5) -> dict[str, Any]:
        """Return waiver wire pickup suggestions."""
        team = self.connector.get_my_team(team_id=team_id)
        waiver_players = sort_players_by_projection(self.connector.get_waiver_wire(limit=25))
        rankings = self.enrichment.get_expert_rankings(
            [player.get("name", "Unknown Player") for player in waiver_players[:limit]]
        )

        context = {
            "team_name": team.get("team_name"),
            "waiver_targets": waiver_players[:limit],
            "expert_rankings": rankings,
        }
        analysis = self.analyzer.suggest_pickups(context)
        return {
            "team_name": team.get("team_name"),
            "pickup_suggestions": waiver_players[:limit],
            "analysis": analysis,
        }
