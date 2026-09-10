"""Common formatting and calculation helpers."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

LINEUP_REQUIREMENTS: dict[str, int] = {
    "QB": 2,
    "RB": 2,
    "WR": 2,
    "TE": 1,
    "FLEX": 1,
}

FLEX_POSITIONS = {"RB", "WR", "TE"}


def sort_players_by_projection(players: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return players ordered by projected points descending."""
    return sorted(players, key=lambda player: float(player.get("projected_points", 0.0) or 0.0), reverse=True)


def group_players_by_position(players: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group players by their listed position."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for player in players:
        grouped[str(player.get("position", "UNK"))].append(player)

    return {position: sort_players_by_projection(entries) for position, entries in grouped.items()}


def build_optimal_lineup(players: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Create a simple optimal lineup for a 2-QB league."""
    grouped = group_players_by_position(players)
    starters: list[dict[str, Any]] = []
    used_names: set[str] = set()

    for position, count in LINEUP_REQUIREMENTS.items():
        if position == "FLEX":
            continue

        for player in grouped.get(position, [])[:count]:
            starters.append(player)
            used_names.add(str(player.get("name")))

    flex_candidates = [
        player
        for position in FLEX_POSITIONS
        for player in grouped.get(position, [])
        if str(player.get("name")) not in used_names
    ]
    for player in sort_players_by_projection(flex_candidates)[: LINEUP_REQUIREMENTS["FLEX"]]:
        starters.append(player)
        used_names.add(str(player.get("name")))

    bench = [player for player in players if str(player.get("name")) not in used_names]
    return starters, bench
