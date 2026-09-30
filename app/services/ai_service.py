import json
import re

from google import genai
from google.genai import types

from app.config import get_settings


def generate_recommendation(prompt: str) -> dict:
    settings = get_settings()

    if not settings.gemini_api_key:
        return {
            "summary": "Gemini API key is not configured.",
            "recommendations": [],
            "source": "fallback",
        }

    client = genai.Client(api_key=settings.gemini_api_key)

    # Try models in order. If one is temporarily unavailable,
    # automatically try the next one.
    models = [
        settings.gemini_model,
        "gemini-2.5-flash",
        "gemini-2.0-flash",
    ]

    last_error = None

    for model in models:
        try:
            print(f"Trying Gemini model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json",
                ),
            )

            text = (response.text or "").strip()

            if not text:
                continue

            text = re.sub(
                r"^```(?:json)?\s*|\s*```$",
                "",
                text,
                flags=re.IGNORECASE,
            ).strip()

            try:
                result = json.loads(text)

                if not isinstance(result, dict):
                    raise ValueError("Gemini response is not a JSON object.")

                result.setdefault("recommendations", [])
                result.setdefault("source", "gemini")

                return result

            except (json.JSONDecodeError, ValueError):
                return {
                    "summary": text,
                    "recommendations": [],
                    "source": "gemini",
                }

        except Exception as exc:
            last_error = exc
            print(f"Gemini model {model} failed: {type(exc).__name__}: {exc}")
            continue

    print("\n========== ALL GEMINI MODELS FAILED ==========")
    print("ERROR:", last_error)
    print("===============================================\n")

    return {
        "summary": "AI service is temporarily unavailable. Please try again.",
        "recommendations": [],
        "source": "fallback",
    }