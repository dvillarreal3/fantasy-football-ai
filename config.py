"""Configuration management for Fantasy Football AI Assistant."""

from __future__ import annotations

import os

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency for local env files
    def load_dotenv() -> bool:
        """Fallback no-op when python-dotenv is unavailable."""
        return False

load_dotenv()

# ESPN Configuration
ESPN_LEAGUE_ID: str | None = os.getenv("ESPN_LEAGUE_ID")
ESPN_S2: str | None = os.getenv("ESPN_S2")
ESPN_SWID: str | None = os.getenv("ESPN_SWID")

# AI Provider Configuration
AI_PROVIDER: str = os.getenv("AI_PROVIDER", "claude").lower()
ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

# Discord Configuration
DISCORD_BOT_TOKEN: str | None = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID: int = int(os.getenv("DISCORD_CHANNEL_ID", 0))

# Optional Data Sources
SLEEPER_API_KEY: str | None = os.getenv("SLEEPER_API_KEY")
FANTASY_PROS_API_KEY: str | None = os.getenv("FANTASY_PROS_API_KEY")

# App Configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

# Recommendation Thresholds
MIN_CONFIDENCE_SCORE = 0.65
TRADE_VALUE_THRESHOLD = 0.1  # 10% improvement
WAIVER_PRIORITY_THRESHOLD = 5  # Top 5 only

# Schedule Configuration
DAILY_REPORT_TIME = "08:00"  # 8 AM
LINEUP_CHECK_TIME = "10:00"  # 10 AM (before games)

# API Endpoints
ESPN_API_BASE = "https://lm-api-reads.fantasy.espn.com/apis/site/v2"
NFL_STATUS_ENDPOINT = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"


def has_ai_provider_key(provider: str | None = None) -> bool:
    """Return whether the requested AI provider has a configured API key."""
    selected_provider = (provider or AI_PROVIDER).lower()
    if selected_provider == "claude":
        return bool(ANTHROPIC_API_KEY)
    if selected_provider == "openai":
        return bool(OPENAI_API_KEY)
    return False


def get_missing_config(*, require_ai: bool = False, require_discord: bool = False) -> list[str]:
    """Return the names of environment variables still needed for a workflow."""
    missing: list[str] = []

    if not ESPN_LEAGUE_ID:
        missing.append("ESPN_LEAGUE_ID")
    if not ESPN_S2:
        missing.append("ESPN_S2")
    if not ESPN_SWID:
        missing.append("ESPN_SWID")

    if require_ai:
        if AI_PROVIDER == "claude" and not ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")
        elif AI_PROVIDER == "openai" and not OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")

    if require_discord:
        if not DISCORD_BOT_TOKEN:
            missing.append("DISCORD_BOT_TOKEN")
        if not DISCORD_CHANNEL_ID:
            missing.append("DISCORD_CHANNEL_ID")

    return missing


def validate_config(*, require_ai: bool = False, require_discord: bool = False) -> bool:
    """Validate runtime configuration for the requested workflow."""
    missing = get_missing_config(require_ai=require_ai, require_discord=require_discord)
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Missing required configuration: {joined}. Check your .env file.")

    return True