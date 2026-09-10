# Fantasy Football AI Assistant

An AI-powered NFL Fantasy Football assistant that provides daily recommendations for lineup optimization, trade targeting, and player pickup suggestions.

## Features

- **Lineup Recommendations**: AI-powered analysis to suggest optimal daily/weekly lineups
- **Trade Targeting**: Identify potential trade partners and analyze trade value
- **Pickup Suggestions**: Get recommendations on which players to add from the waiver wire
- **News Integration**: Real-time injury reports and player news consideration
- **Discord Delivery**: Automated daily reports sent directly to Discord
- **Multi-League Support**: Manage multiple fantasy leagues

## Tech Stack

- **Python 3.9+**
- **LLM Integration**: Claude (Anthropic) or OpenAI GPT for AI analysis
- **ESPN API**: Reverse-engineered via `espn-api` library
- **Discord Bot**: discord.py for report delivery
- **Data Sources**: Multiple fantasy sports APIs for enriched player data

## Prerequisites

- Python 3.9 or higher
- ESPN Fantasy Football league
- Discord server and bot token (for notifications)
- API key for Claude or OpenAI
- ESPN authentication credentials (SWID and ESPN_S2 cookies)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dvillarreal3/fantasy-football-ai.git
cd fantasy-football-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your credentials:
```
# ESPN Credentials
ESPN_LEAGUE_ID=your_league_id
ESPN_S2=your_espn_s2_cookie
ESPN_SWID=your_espn_swid_cookie

# AI Provider (choose one)
OPENAI_API_KEY=your_openai_key
# OR
ANTHROPIC_API_KEY=your_claude_key

# Discord
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_target_channel_id

# Optional: External Data Sources
SLEEPER_API_KEY=optional
FANTASY_PROS_API_KEY=optional
```

## First Local Setup Order

Use this order to keep setup simple and isolate failures:

1. Create a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Fill in ESPN credentials first:
   - `ESPN_LEAGUE_ID`
   - `ESPN_S2`
   - `ESPN_SWID`
5. Add one AI provider key:
   - `ANTHROPIC_API_KEY` for Claude
   - or `OPENAI_API_KEY` for OpenAI
6. Run the setup check:
```bash
python main.py check
```
7. Run one manual report before enabling Discord or scheduling:
```bash
python main.py lineup
```
8. If the report works, test Discord delivery:
```bash
python main.py lineup --discord
```
9. Only after that, enable scheduled runs:
```bash
python main.py lineup --schedule --time 08:00
```

## Getting ESPN Credentials

1. Open ESPN Fantasy Football in your browser
2. Open Developer Tools (F12 or Right-click → Inspect)
3. Go to Application → Cookies
4. Find and copy:
   - `ESPN_S2` cookie value
   - `SWID` cookie value (usually in format `{uuid}`)
5. Your league ID is in the URL: `www.espn.com/fantasy/football/league?leagueId=YOUR_LEAGUE_ID`

## Usage

### Basic Setup
```python
from fantasy_ai import FantasyAssistant

assistant = FantasyAssistant(
    league_id="YOUR_LEAGUE_ID",
    ai_provider="claude"  # or "openai"
)

# Get lineup recommendations
recommendations = assistant.get_lineup_recommendations()

# Get trade suggestions
trades = assistant.analyze_trade_opportunities()

# Get pickup suggestions
pickups = assistant.get_pickup_suggestions()
```

### Running Automated Reports
```bash
# Run daily at 8 AM
python main.py lineup --schedule --time 08:00
```

### Checking Local Setup
```bash
python main.py check
```

This prints whether core ESPN settings are present, whether your selected AI provider is configured for live responses, and whether Discord is ready.

## Project Structure

```
fantasy-football-ai/
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── main.py
├── fantasy_ai/
│   ├── __init__.py
│   ├── espn_connector.py      # ESPN API integration
│   ├── ai_analyzer.py         # AI-powered analysis
│   ├── data_enrichment.py     # External data sources
│   ├── recommendations.py     # Recommendation logic
│   └── discord_notifier.py    # Discord integration
├── tests/
│   ├── test_espn_connector.py
│   ├── test_ai_analyzer.py
│   └── test_recommendations.py
└── utils/
    ├── logger.py
    └── helpers.py
```

## Configuration

Edit `config.py` to customize:
- AI analysis prompts and style
- Recommendation thresholds
- Discord message formatting
- Scheduling preferences
- Data source priorities

## Optional Local Dashboard

Adding a local dashboard is very feasible because the repository already separates data access, recommendation logic, and delivery.

Recommended order:
1. Get one local CLI report working first.
2. Keep lineup, trade, and pickup outputs in stable dictionary structures.
3. Add a lightweight dashboard layer on top of those outputs.

Good options:
- **Streamlit** for the fastest personal dashboard
- **FastAPI + frontend** for a cleaner long-term application structure

Suggested first dashboard views:
- roster overview
- lineup recommendations
- waiver wire suggestions
- injury and news summaries

## How It Works

1. **Data Collection**: Fetches your league data, roster, waiver wire, and player stats
2. **Enrichment**: Integrates real-time news, injury reports, and expert rankings
3. **AI Analysis**: Uses Claude/GPT to analyze opportunities with full context
4. **Recommendations**: Generates actionable insights for lineup, trades, and pickups
5. **Delivery**: Sends formatted reports to Discord daily

## Limitations & Notes

- ESPN does not officially support third-party API access; this uses reverse-engineered endpoints
- Recommendations are suggestions only—always review before making moves
- Some features may break if ESPN changes their infrastructure
- Respect ESPN's Terms of Service and league rules

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License—see the LICENSE file for details.

## Support & Troubleshooting

For common issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

Questions or need help? Open an [Issue](https://github.com/dvillarreal3/fantasy-football-ai/issues)

## Disclaimer

This tool is for entertainment and educational purposes. Always make your own decisions about fantasy league moves. The creator is not responsible for any losses or adverse outcomes resulting from recommendations provided by this tool.
