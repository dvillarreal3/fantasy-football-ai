"""Helpers for pulling external player context data."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import requests


@dataclass
class DataEnrichment:
    """Fetch supplemental news, injury, and ranking data."""

    session: requests.Session = field(default_factory=requests.Session)
    timeout: int = 10
    news_base_url: str = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"

    def get_player_news(self, player_name: str) -> list[dict[str, Any]]:
        """Fetch recent articles for a player, returning an empty list on failure."""
        return self._fetch_items(
            url=f"{self.news_base_url}/news",
            params={"limit": 10, "search": player_name},
            item_key="articles",
        )

    def get_injury_reports(self, player_name: Optional[str] = None) -> list[dict[str, Any]]:
        """Fetch basic injury report data, optionally filtered by player name."""
        reports = self._fetch_items(
            url=f"{self.news_base_url}/injuries",
            params={},
            item_key="injuries",
        )
        if not player_name:
            return reports

        normalized = player_name.lower()
        return [report for report in reports if normalized in str(report).lower()]

    def get_expert_rankings(self, players: list[str]) -> list[dict[str, Any]]:
        """Return a lightweight consensus ranking placeholder for the given players."""
        # TODO: Replace this placeholder with a real expert rankings source.
        return [
            {"player_name": player, "consensus_rank": index + 1, "source": "local-placeholder"}
            for index, player in enumerate(players)
        ]

    def _fetch_items(
        self,
        *,
        url: str,
        params: dict[str, Any],
        item_key: str,
    ) -> list[dict[str, Any]]:
        """Perform a GET request and normalize list-like payloads."""
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException:
            return []

        payload = response.json()
        items = payload.get(item_key, [])
        return [item for item in items if isinstance(item, dict)]
