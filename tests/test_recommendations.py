"""Unit tests for the recommendation engine."""

import unittest

from fantasy_ai.ai_analyzer import AIAnalyzer
from fantasy_ai.recommendations import RecommendationEngine


class _Connector:
    def get_my_team(self, team_id: int | None = None) -> dict:
        return {
            "team_name": "Roster Builders",
            "roster": [
                {"name": "Josh Allen", "position": "QB", "projected_points": 24.0},
                {"name": "Dak Prescott", "position": "QB", "projected_points": 21.5},
                {"name": "Bijan Robinson", "position": "RB", "projected_points": 18.0},
                {"name": "James Cook", "position": "RB", "projected_points": 15.5},
                {"name": "CeeDee Lamb", "position": "WR", "projected_points": 19.0},
                {"name": "Amon-Ra St. Brown", "position": "WR", "projected_points": 18.7},
                {"name": "Sam LaPorta", "position": "TE", "projected_points": 13.0},
                {"name": "Rhamondre Stevenson", "position": "RB", "projected_points": 11.1},
            ],
        }

    def get_waiver_wire(self, limit: int = 25) -> list[dict]:
        return [
            {"name": "Tyjae Spears", "position": "RB", "projected_points": 10.5},
            {"name": "Rome Odunze", "position": "WR", "projected_points": 9.8},
        ][:limit]


class _Enrichment:
    def get_player_news(self, player_name: str) -> list[dict]:
        return []

    def get_injury_reports(self, player_name: str | None = None) -> list[dict]:
        return []

    def get_expert_rankings(self, players: list[str]) -> list[dict]:
        return [{"player_name": player, "consensus_rank": index + 1} for index, player in enumerate(players)]


class RecommendationEngineTests(unittest.TestCase):
    """Tests for deterministic recommendation logic."""

    def setUp(self) -> None:
        """Create a reusable recommendation engine fixture."""
        self.engine = RecommendationEngine(
            connector=_Connector(),
            analyzer=AIAnalyzer(),
            enrichment=_Enrichment(),
        )

    def test_lineup_recommendations_prioritize_two_qb_build(self) -> None:
        """The lineup optimizer should fill the two QB slots first."""
        result = self.engine.get_lineup_recommendations()

        qbs = [player for player in result["recommended_starters"] if player["position"] == "QB"]
        self.assertEqual(len(qbs), 2)
        self.assertEqual(qbs[0]["name"], "Josh Allen")

    def test_pickup_suggestions_limit_results(self) -> None:
        """Pickup suggestions should respect the requested limit."""
        result = self.engine.get_pickup_suggestions(limit=1)

        self.assertEqual(len(result["pickup_suggestions"]), 1)
        self.assertEqual(result["pickup_suggestions"][0]["name"], "Tyjae Spears")


if __name__ == "__main__":
    unittest.main()
