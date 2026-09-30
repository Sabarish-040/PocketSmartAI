from app.services.ai_service import generate_recommendation
from app.services.catalog_service import (
    home_catalog,
    jewelry_catalog,
    party_catalog,
)


def build_home_plan(
    budget: float,
    room: str,
    style: str,
    items: str,
) -> dict:

    catalog = home_catalog(room, budget)

    prompt = f"""
Create a practical home budget plan.

Budget: {budget}
Room: {room}
Style: {style}
Items: {items}

Return ONLY valid JSON in this exact format:

{{
  "summary": "A useful 2-3 sentence home plan",
  "recommendations": [
    {{
      "name": "item name",
      "category": "category",
      "estimated_price": 0,
      "platform": "platform",
      "url": "",
      "reason": "why this item is recommended"
    }}
  ]
}}
"""

    ai = generate_recommendation(prompt)

    ai_summary = ai.get("summary")

    # Use Gemini recommendations when available.
    ai_recommendations = ai.get("recommendations", [])

    if ai_recommendations:
        recommendations = ai_recommendations
    else:
        recommendations = [
            {
                **item,
                "reason": "Fits the selected home budget.",
            }
            for item in catalog
        ]

    return {
        "planner": "home",
        "budget": budget,
        "summary": ai_summary or "Home plan created successfully.",
        "allocation": {
            item["category"]: item["estimated_price"]
            for item in catalog
        },
        "recommendations": recommendations,
        "disclaimer": "Prices are estimates and may change.",
        "source": ai.get("source", "catalog"),
    }


def build_party_plan(
    budget: float,
    guests: int,
    event_type: str,
    venue: str,
) -> dict:

    catalog = party_catalog(
        event_type,
        guests,
        budget,
    )

    prompt = f"""
Create a practical party budget plan.

Budget: {budget}
Guests: {guests}
Event: {event_type}
Venue: {venue}

Return ONLY valid JSON in this exact format:

{{
  "summary": "A useful 2-3 sentence party plan",
  "recommendations": []
}}
"""

    ai = generate_recommendation(prompt)

    return {
        "planner": "party",
        "budget": budget,
        "summary": ai.get(
            "summary",
            "Party plan created successfully.",
        ),
        "allocation": {
            item["category"]: item["estimated_price"]
            for item in catalog
        },
        "recommendations": [
            {
                **item,
                "reason": "Fits the selected party budget.",
            }
            for item in catalog
        ],
        "disclaimer": "Prices are estimates and may change.",
        "source": ai.get("source", "catalog"),
    }


def build_jewelry_plan(budget: float) -> dict:

    catalog = jewelry_catalog(budget)

    prompt = f"""
Create a practical jewelry shopping recommendation.

Budget: {budget}

Return ONLY valid JSON in this exact format:

{{
  "summary": "A useful 2-3 sentence jewelry plan",
  "recommendations": []
}}
"""

    ai = generate_recommendation(prompt)

    return {
        "planner": "jewelry",
        "budget": budget,
        "summary": ai.get(
            "summary",
            "Jewelry plan created successfully.",
        ),
        "allocation": {
            item["category"]: item["estimated_price"]
            for item in catalog
        },
        "recommendations": [
            {
                **item,
                "reason": "Fits the selected jewelry budget.",
            }
            for item in catalog
        ],
        "disclaimer": "Prices are estimates and may change.",
        "source": ai.get("source", "catalog"),
    }