"""
Configuration management for Fantasy Football AI Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ESPN Configuration
ESPN_LEAGUE_ID = os.getenv("ESPN_LEAGUE_ID")
ESPN_S2 = os.getenv("ESPN_S2")
ESPN_SWID = os.getenv("ESPN_SWID")

# AI Provider Configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "claude").lower()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Discord Configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", 0))

# Optional Data Sources
SLEEPER_API_KEY = os.getenv("SLEEPER_API_KEY")
FANTASY_PROS_API_KEY = os.getenv("FANTASY_PROS_API_KEY")

# App Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

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

def validate_config():
    """Validate required configuration"""
    required = [ESPN_LEAGUE_ID, ESPN_S2, ESPN_SWID, DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID]
    if AI_PROVIDER == "claude":
        required.append(ANTHROPIC_API_KEY)
    elif AI_PROVIDER == "openai":
        required.append(OPENAI_API_KEY)
    
    missing = [config for config in required if not config]
    if missing:
        raise ValueError("Missing required configuration. Check your .env file.")
    
    return True