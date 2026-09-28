def home_catalog(room: str, budget: float) -> list[dict]:
    data = [
        ("LED lighting", "Lighting", budget * 0.15, "Amazon"),
        ("Ceiling fan", "Electrical", budget * 0.20, "Flipkart"),
        ("Home decor", "Decor", budget * 0.20, "Amazon"),
        ("Storage furniture", "Furniture", budget * 0.30, "IKEA"),
        ("Curtains and accessories", "Decor", budget * 0.15, "Myntra"),
    ]

    return [
        {
            "name": name,
            "category": category,
            "estimated_price": round(price, 2),
            "platform": platform,
            "url": "#",
        }
        for name, category, price, platform in data
    ]


def party_catalog(
    event_type: str,
    guests: int,
    budget: float,
) -> list[dict]:
    data = [
        ("Catering package", "Catering", budget * 0.40, "Swiggy"),
        ("Food ordering options", "Food", budget * 0.20, "Zomato"),
        ("Event decoration", "Decoration", budget * 0.15, "Amazon"),
        ("Venue and accommodation", "Venue", budget * 0.20, "OYO"),
        ("Party lighting", "Entertainment", budget * 0.05, "Flipkart"),
    ]

    return [
        {
            "name": name,
            "category": category,
            "estimated_price": round(price, 2),
            "platform": platform,
            "url": "#",
        }
        for name, category, price, platform in data
    ]


def jewelry_catalog(budget: float) -> list[dict]:
    data = [
        ("Everyday earrings", "Earrings", budget * 0.15, "Myntra"),
        ("Classic necklace", "Necklace", budget * 0.35, "Amazon"),
        ("Bracelet", "Bracelet", budget * 0.20, "Flipkart"),
        ("Ring", "Ring", budget * 0.20, "Amazon"),
        ("Jewelry storage box", "Accessory", budget * 0.10, "Myntra"),
    ]

    return [
        {
            "name": name,
            "category": category,
            "estimated_price": round(price, 2),
            "platform": platform,
            "url": "#",
        }
        for name, category, price, platform in data
    ]