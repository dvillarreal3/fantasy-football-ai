"""Unit tests for configuration helpers."""

import unittest
from unittest.mock import patch

import config


class ConfigTests(unittest.TestCase):
    """Tests for runtime configuration validation."""

    def test_get_missing_config_only_requires_core_for_local_report(self) -> None:
        """Discord and AI should stay optional for a basic local report."""
        with patch.object(config, "ESPN_LEAGUE_ID", "1"), patch.object(config, "ESPN_S2", "s2"), patch.object(
            config, "ESPN_SWID", "{swid}"
        ):
            self.assertEqual(config.get_missing_config(), [])

    def test_get_missing_config_requires_discord_when_requested(self) -> None:
        """Discord variables should only be required for Discord workflows."""
        with patch.object(config, "ESPN_LEAGUE_ID", "1"), patch.object(config, "ESPN_S2", "s2"), patch.object(
            config, "ESPN_SWID", "{swid}"
        ), patch.object(config, "DISCORD_BOT_TOKEN", None), patch.object(config, "DISCORD_CHANNEL_ID", 0):
            self.assertEqual(
                config.get_missing_config(require_discord=True),
                ["DISCORD_BOT_TOKEN", "DISCORD_CHANNEL_ID"],
            )

    def test_has_ai_provider_key_checks_selected_provider(self) -> None:
        """AI provider key detection should match the configured provider."""
        with patch.object(config, "AI_PROVIDER", "openai"), patch.object(config, "OPENAI_API_KEY", "key"):
            self.assertTrue(config.has_ai_provider_key())


if __name__ == "__main__":
    unittest.main()
