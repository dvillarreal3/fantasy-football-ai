"""Unit tests for the ESPN connector module."""

import unittest

from fantasy_ai.espn_connector import ESPNConnector


class _Player:
    def __init__(self, name: str, position: str, projected_points: float) -> None:
        self.name = name
        self.position = position
        self.projected_points = projected_points
        self.total_points = projected_points


class _Team:
    def __init__(self) -> None:
        self.team_id = 1
        self.team_name = "Test Team"
        self.owners = ["manager"]
        self.roster = [_Player("Josh Allen", "QB", 24.0)]


class _League:
    def __init__(self) -> None:
        self.teams = [_Team()]

    def free_agents(self, size: int = 25) -> list[_Player]:
        return [_Player("Jordan Mason", "RB", 12.3)][:size]


class ESPNConnectorTests(unittest.TestCase):
    """Tests for the ESPN connector wrapper."""

    def test_espn_connector_returns_team_and_player_data(self) -> None:
        """The connector should normalize league and player objects."""
        connector = ESPNConnector(league_id=1, espn_s2="s2", swid="{swid}")
        connector._league = _League()

        team = connector.get_my_team()
        player = connector.get_player_stats("Jordan Mason")

        self.assertEqual(team["team_name"], "Test Team")
        self.assertEqual(team["roster"][0]["name"], "Josh Allen")
        self.assertEqual(player["position"], "RB")


if __name__ == "__main__":
    unittest.main()
