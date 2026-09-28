import json

from google import genai

from app.config import get_settings


def generate_recommendation(prompt: str) -> dict:
    settings = get_settings()

    if not settings.gemini_api_key:
        return {
            "summary": "AI recommendations are not configured yet.",
            "recommendations": [],
            "source": "fallback",
        }

    try:
        client = genai.Client(
            api_key=settings.gemini_api_key
        )

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )

        text = response.text or ""

        try:
            return json.loads(text)

        except json.JSONDecodeError:
            return {
                "summary": text,
                "recommendations": [],
                "source": "gemini",
            }

    except Exception as exc:
        return {
            "summary": "AI service is temporarily unavailable.",
            "recommendations": [],
            "source": "fallback",
            "error": str(exc),
        }