"""CLI entry point for the Fantasy Football AI assistant."""

from __future__ import annotations

import argparse
from typing import Callable

from config import (
    AI_PROVIDER,
    ANTHROPIC_API_KEY,
    DAILY_REPORT_TIME,
    DISCORD_BOT_TOKEN,
    DISCORD_CHANNEL_ID,
    ESPN_LEAGUE_ID,
    ESPN_S2,
    ESPN_SWID,
    OPENAI_API_KEY,
)
from fantasy_ai import FantasyAssistant
from utils.logger import configure_logging, get_logger

LOGGER = get_logger(__name__)


def build_assistant() -> FantasyAssistant:
    """Construct the main assistant from environment configuration."""
    if not ESPN_LEAGUE_ID:
        raise ValueError("ESPN_LEAGUE_ID is required before running reports.")

    ai_api_key = ANTHROPIC_API_KEY if AI_PROVIDER == "claude" else OPENAI_API_KEY
    return FantasyAssistant(
        league_id=ESPN_LEAGUE_ID,
        ai_provider=AI_PROVIDER,
        espn_s2=ESPN_S2,
        swid=ESPN_SWID,
        ai_api_key=ai_api_key,
        discord_token=DISCORD_BOT_TOKEN,
        discord_channel_id=DISCORD_CHANNEL_ID or None,
    )


def run_manual_report(report_type: str, send_to_discord: bool = False) -> dict:
    """Run one report immediately and optionally send it to Discord."""
    assistant = build_assistant()
    report_handlers: dict[str, Callable[[], dict]] = {
        "lineup": assistant.get_lineup_recommendations,
        "trade": assistant.analyze_trade_opportunities,
        "pickup": assistant.get_pickup_suggestions,
    }
    report = report_handlers[report_type]()
    LOGGER.info("Generated %s report for %s", report_type, report.get("team_name", "unknown team"))

    if send_to_discord:
        sender = {
            "lineup": assistant.notifier.send_lineup_report,
            "trade": assistant.notifier.send_trade_report,
            "pickup": assistant.notifier.send_pickup_report,
        }[report_type]
        sender(report)

    return report


def schedule_daily_reports(report_type: str, schedule_time: str) -> None:
    """Schedule a report with APScheduler and keep the process alive."""
    try:
        from apscheduler.schedulers.blocking import BlockingScheduler
    except ImportError as exc:
        raise RuntimeError("APScheduler is required for scheduled runs.") from exc

    hour, minute = schedule_time.split(":", maxsplit=1)
    scheduler = BlockingScheduler()
    scheduler.add_job(
        lambda: run_manual_report(report_type, send_to_discord=True),
        trigger="cron",
        hour=int(hour),
        minute=int(minute),
    )
    LOGGER.info("Scheduled %s report for %s each day.", report_type, schedule_time)
    # TODO: add support for multiple daily jobs and timezone configuration.
    scheduler.start()


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Fantasy Football AI assistant")
    parser.add_argument(
        "report_type",
        choices=["lineup", "trade", "pickup"],
        help="Type of report to generate.",
    )
    parser.add_argument("--discord", action="store_true", help="Send the report to Discord.")
    parser.add_argument("--schedule", action="store_true", help="Run the report on a daily schedule.")
    parser.add_argument(
        "--time",
        default=DAILY_REPORT_TIME,
        help="Daily schedule time in HH:MM format. Defaults to config DAILY_REPORT_TIME.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the CLI application."""
    configure_logging()
    try:
        args = parse_args()

        if args.schedule:
            schedule_daily_reports(args.report_type, args.time)
            return 0

        report = run_manual_report(args.report_type, send_to_discord=args.discord)
        print(report)
        return 0
    except Exception as exc:
        LOGGER.error("Fantasy Football AI run failed: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
