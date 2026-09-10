"""Unit tests for the CLI entry point."""

import unittest
from unittest.mock import patch

import main


class MainTests(unittest.TestCase):
    """Tests for setup-oriented CLI behavior."""

    def test_run_setup_check_reports_missing_core_configuration(self) -> None:
        """The setup check should surface missing ESPN variables."""
        with patch.object(main, "ESPN_LEAGUE_ID", None), patch.object(main, "ESPN_S2", None), patch.object(
            main, "ESPN_SWID", None
        ):
            result = main.run_setup_check()

        self.assertFalse(result["core_configured"])
        self.assertIn("ESPN_LEAGUE_ID", result["missing_core"])

    def test_run_setup_check_reports_live_ai_and_discord_status(self) -> None:
        """The setup check should describe AI and Discord readiness."""
        with patch.object(main, "validate_config", return_value=True), patch.object(
            main, "has_ai_provider_key", return_value=True
        ), patch.object(main, "DISCORD_BOT_TOKEN", "token"), patch.object(main, "DISCORD_CHANNEL_ID", 1234):
            result = main.run_setup_check()

        self.assertTrue(result["core_configured"])
        self.assertTrue(result["ai_live"])
        self.assertTrue(result["discord_configured"])


if __name__ == "__main__":
    unittest.main()
