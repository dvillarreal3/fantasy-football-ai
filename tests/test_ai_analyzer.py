"""Unit tests for the AI analyzer module."""

import unittest

from fantasy_ai.ai_analyzer import AIAnalyzer


class AIAnalyzerTests(unittest.TestCase):
    """Tests for the AI analyzer facade."""

    def test_ai_analyzer_uses_fallback_without_api_key(self) -> None:
        """The analyzer should remain usable when credentials are missing."""
        analyzer = AIAnalyzer(provider="claude")

        result = analyzer.analyze_lineup({"starters": [{"name": "Josh Allen"}]})

        self.assertEqual(result["provider"], "fallback")
        self.assertIn("configure an API key", result["summary"])


if __name__ == "__main__":
    unittest.main()
