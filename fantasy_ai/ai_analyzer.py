"""LLM-backed analysis helpers for fantasy recommendations."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping, Optional


class AIAnalyzerError(RuntimeError):
    """Raised when the configured AI provider cannot complete a request."""


@dataclass
class AIAnalyzer:
    """Provide a unified interface across Anthropic and OpenAI chat models."""

    provider: str = "claude"
    api_key: Optional[str] = None
    model: Optional[str] = None

    def __post_init__(self) -> None:
        """Normalize provider settings and select a default model."""
        self.provider = self.provider.lower()
        if not self.model:
            self.model = "claude-3-5-sonnet-latest" if self.provider == "claude" else "gpt-4o-mini"

    def analyze_lineup(self, lineup_context: Mapping[str, Any]) -> dict[str, Any]:
        """Analyze a lineup context and return structured advice."""
        prompt = self._build_prompt("lineup optimization", lineup_context)
        return self._request_analysis(prompt, fallback_title="Lineup analysis")

    def evaluate_trades(self, trade_context: Mapping[str, Any]) -> dict[str, Any]:
        """Analyze trade opportunities and return structured advice."""
        prompt = self._build_prompt("trade evaluation", trade_context)
        return self._request_analysis(prompt, fallback_title="Trade analysis")

    def suggest_pickups(self, waiver_context: Mapping[str, Any]) -> dict[str, Any]:
        """Analyze waiver targets and return structured advice."""
        prompt = self._build_prompt("waiver wire pickups", waiver_context)
        return self._request_analysis(prompt, fallback_title="Pickup analysis")

    def _request_analysis(self, prompt: str, fallback_title: str) -> dict[str, Any]:
        """Send the prompt to the configured provider or return a safe fallback."""
        if not self.api_key:
            return self._fallback_response(fallback_title, prompt)

        if self.provider == "claude":
            return self._call_anthropic(prompt, fallback_title)
        if self.provider == "openai":
            return self._call_openai(prompt, fallback_title)
        raise AIAnalyzerError(f"Unsupported AI provider: {self.provider}")

    def _call_anthropic(self, prompt: str, fallback_title: str) -> dict[str, Any]:
        """Call Anthropic's Messages API."""
        try:
            from anthropic import Anthropic
        except ImportError:
            return self._fallback_response(fallback_title, prompt)

        client = Anthropic(api_key=self.api_key)
        try:
            response = client.messages.create(
                model=self.model or "claude-3-5-sonnet-latest",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as exc:  # pragma: no cover - third-party dependency
            raise AIAnalyzerError(f"Anthropic request failed: {exc}") from exc

        text = " ".join(
            block.text for block in getattr(response, "content", []) if hasattr(block, "text")
        ).strip()
        return {"provider": "claude", "model": self.model, "summary": text, "raw_response": response}

    def _call_openai(self, prompt: str, fallback_title: str) -> dict[str, Any]:
        """Call OpenAI's Responses API."""
        try:
            from openai import OpenAI
        except ImportError:
            return self._fallback_response(fallback_title, prompt)

        client = OpenAI(api_key=self.api_key)
        try:
            response = client.responses.create(model=self.model or "gpt-4o-mini", input=prompt)
        except Exception as exc:  # pragma: no cover - third-party dependency
            raise AIAnalyzerError(f"OpenAI request failed: {exc}") from exc

        text = getattr(response, "output_text", "").strip()
        return {"provider": "openai", "model": self.model, "summary": text, "raw_response": response}

    @staticmethod
    def _build_prompt(topic: str, context: Mapping[str, Any]) -> str:
        """Build a consistent prompt for football-specific analysis."""
        return (
            "You are a fantasy football assistant for a 12-team, 2-QB NFL league.\n"
            f"Provide concise, actionable advice for {topic}.\n"
            "Call out risk, upside, and the top recommendation first.\n"
            f"Context:\n{json.dumps(dict(context), indent=2, default=str)}"
        )

    @staticmethod
    def _fallback_response(title: str, prompt: str) -> dict[str, Any]:
        """Return a deterministic placeholder until live AI credentials are configured."""
        return {
            "provider": "fallback",
            "model": "local-template",
            "summary": (
                f"{title}: configure an API key to enable live model responses. "
                "This fallback keeps the application testable while integrations are unfinished."
            ),
            "prompt_preview": prompt[:500],
            "todo": "TODO: expand deterministic fallback logic for offline recommendation scoring.",
        }
