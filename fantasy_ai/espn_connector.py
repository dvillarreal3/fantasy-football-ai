"""ESPN Fantasy Football integration helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


class ESPNConnectorError(RuntimeError):
    """Raised when ESPN league data cannot be retrieved."""


@dataclass
class ESPNConnector:
    """Wrapper around the `espn-api` football client."""

    league_id: int | str
    year: Optional[int] = None
    espn_s2: Optional[str] = None
    swid: Optional[str] = None

    def __post_init__(self) -> None:
        """Normalize constructor inputs for later API requests."""
        self.league_id = int(self.league_id)
        self._league: Any | None = None

    def get_league(self) -> Any:
        """Return the underlying ESPN league object, creating it on first use."""
        if self._league is not None:
            return self._league

        if not self.espn_s2 or not self.swid:
            raise ESPNConnectorError("ESPN authentication requires both ESPN_S2 and SWID.")

        try:
            from espn_api.football import League
        except ImportError as exc:
            raise ESPNConnectorError(
                "The `espn-api` package is required to fetch league data."
            ) from exc

        league_kwargs: dict[str, Any] = {
            "league_id": self.league_id,
            "espn_s2": self.espn_s2,
            "swid": self.swid,
        }
        if self.year is not None:
            league_kwargs["year"] = self.year

        try:
            self._league = League(**league_kwargs)
        except Exception as exc:  # pragma: no cover - network/auth dependency
            raise ESPNConnectorError(f"Unable to initialize ESPN league: {exc}") from exc

        return self._league

    def get_my_team(self, team_id: Optional[int] = None) -> dict[str, Any]:
        """Return roster data for a specific team or the first team in the league."""
        league = self.get_league()
        teams = list(getattr(league, "teams", []))
        if not teams:
            raise ESPNConnectorError("No teams were returned by the ESPN league.")

        team = next((entry for entry in teams if getattr(entry, "team_id", None) == team_id), teams[0])
        return {
            "team_id": getattr(team, "team_id", None),
            "team_name": getattr(team, "team_name", "Unknown Team"),
            "owner": getattr(team, "owners", []),
            "roster": [self._player_to_dict(player) for player in getattr(team, "roster", [])],
        }

    def get_waiver_wire(self, limit: int = 25) -> list[dict[str, Any]]:
        """Return free agents from the waiver wire."""
        league = self.get_league()
        try:
            players = league.free_agents(size=limit)
        except Exception as exc:  # pragma: no cover - network/auth dependency
            raise ESPNConnectorError(f"Unable to fetch waiver wire: {exc}") from exc

        return [self._player_to_dict(player) for player in players]

    def get_player_stats(self, player_name: str) -> dict[str, Any]:
        """Return a flattened player stats payload for a named player."""
        normalized_name = player_name.strip().lower()

        roster = self.get_my_team().get("roster", [])
        for player in roster + self.get_waiver_wire(limit=100):
            if str(player.get("name", "")).strip().lower() == normalized_name:
                return player

        raise ESPNConnectorError(f"Player '{player_name}' was not found in roster or waiver wire.")

    @staticmethod
    def _player_to_dict(player: Any) -> dict[str, Any]:
        """Convert an `espn-api` player object into a serializable dictionary."""
        return {
            "name": getattr(player, "name", "Unknown Player"),
            "position": getattr(player, "position", "UNK"),
            "pro_team": getattr(player, "proTeam", None),
            "injury_status": getattr(player, "injuryStatus", None),
            "projected_points": float(getattr(player, "projected_points", 0.0) or 0.0),
            "points": float(getattr(player, "total_points", 0.0) or 0.0),
        }
