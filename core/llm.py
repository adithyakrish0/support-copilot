"""Provider-agnostic chat client.

Works with any OpenAI-compatible endpoint (Groq, OpenRouter, Cerebras, OpenAI...).
Everything is configured through environment variables so the provider can be
swapped without touching the code:

    LLM_API_KEY   - your key
    LLM_BASE_URL  - e.g. https://api.groq.com/openai/v1
    LLM_MODEL     - e.g. llama-3.3-70b-versatile

If LLM_API_KEY is empty the app runs in MOCK MODE: no network calls, and
`core.triage` falls back to rule-based logic. This keeps the demo runnable
by anyone who clones the repo.
"""

from __future__ import annotations

import json
import os
import re

from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "llama-3.3-70b-versatile"


def config() -> dict:
    """Return the resolved provider configuration."""
    api_key = os.getenv("LLM_API_KEY", "").strip()
    return {
        "api_key": api_key,
        "base_url": os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL).strip(),
        "model": os.getenv("LLM_MODEL", DEFAULT_MODEL).strip(),
        "live": bool(api_key),
    }


def chat(messages: list[dict], temperature: float = 0.2) -> str:
    """Send a chat completion request and return the raw text response.

    Raises RuntimeError if called without a key; callers should check
    `config()["live"]` first.
    """
    cfg = config()
    if not cfg["live"]:
        raise RuntimeError("LLM_API_KEY is not set - running in mock mode.")

    from openai import OpenAI

    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
    response = client.chat.completions.create(
        model=cfg["model"],
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def parse_json(raw: str) -> dict:
    """Parse JSON out of a model response, tolerating ```json fences."""
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Last resort: grab the outermost {...} block.
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        return json.loads(text[start : end + 1])
    raise ValueError(f"Model did not return valid JSON: {raw[:200]}")
