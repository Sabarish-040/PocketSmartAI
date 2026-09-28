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

    prompt = (
        f"Create a simple home budget recommendation. "
        f"Budget: {budget}. Room: {room}. Style: {style}. "
        f"Items: {items}. Give practical advice."
    )

    ai = generate_recommendation(prompt)

    return {
        "planner": "home",
        "budget": budget,
        "summary": ai.get(
            "summary",
            "Home plan created successfully.",
        ),
        "allocation": {
            item["category"]: item["estimated_price"]
            for item in catalog
        },
        "recommendations": [
            {
                **item,
                "reason": "Fits the selected home budget.",
            }
            for item in catalog
        ],
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

    prompt = (
        f"Create a simple party budget recommendation. "
        f"Budget: {budget}. Guests: {guests}. "
        f"Event: {event_type}. Venue: {venue}. "
        f"Give practical advice."
    )

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

    prompt = (
        f"Create a simple jewelry shopping recommendation. "
        f"Budget: {budget}. Give practical advice."
    )

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