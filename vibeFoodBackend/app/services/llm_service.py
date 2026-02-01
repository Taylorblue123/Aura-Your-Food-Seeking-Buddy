"""
Fake LLM service for MVP testing.
Returns predefined recommendations instead of actual GPT-4 processing.
"""
from datetime import datetime
from typing import List
from uuid import uuid4

from app.models.domain import (
    MenuData,
    VibeData,
    Recommendation,
    RecommendationSet,
)
from app.models.enums import VibeType


# Vibe-to-dish mapping for fake recommendations
VIBE_DISH_MAPPING = {
    VibeType.COMFORT: ["Massaman Curry", "Pad Thai"],
    VibeType.ADVENTURE: ["Tom Yum Soup", "Green Curry"],
    VibeType.LIGHT: ["Tom Yum Soup", "Spring Rolls"],
    VibeType.QUICK: ["Pad Thai", "Spring Rolls"],
    VibeType.SHARING: ["Spring Rolls", "Pad Thai"],
    VibeType.BUDGET: ["Spring Rolls", "Pad Thai"],
    VibeType.HEALTHY: ["Tom Yum Soup", "Spring Rolls"],
    VibeType.INDULGENT: ["Mango Sticky Rice", "Massaman Curry"],
}

DISH_REASONS = {
    "Pad Thai": "A beloved classic that delivers satisfying flavors with its perfect balance of sweet, sour, and savory notes.",
    "Green Curry": "An exciting flavor journey with aromatic Thai basil and creamy coconut that will awaken your taste buds.",
    "Tom Yum Soup": "A vibrant, aromatic soup that's both refreshing and deeply flavorful - perfect for a lighter option.",
    "Mango Sticky Rice": "A heavenly dessert that's pure comfort in every bite - sweet mango meets creamy coconut rice.",
    "Spring Rolls": "Crispy, light, and perfect for sharing - a crowd-pleaser that won't weigh you down.",
    "Massaman Curry": "Rich, warming, and deeply comforting - like a hug in a bowl with tender meat and potatoes.",
}


async def generate_recommendations(
    menu_data: MenuData,
    vibe_data: VibeData,
) -> RecommendationSet:
    """
    Fake LLM recommendation generation.
    In production, this would call OpenAI GPT-4.

    Args:
        menu_data: The extracted menu data
        vibe_data: User's vibe selection and constraints

    Returns:
        RecommendationSet with fake recommendations based on vibe mapping
    """
    recommendations: List[Recommendation] = []
    seen_dishes = set()

    # Map menu items by name for lookup
    menu_items_by_name = {item.name: item for item in menu_data.items}

    # Get recommendations based on selected vibes
    for vibe in vibe_data.vibes:
        vibe_enum = vibe if isinstance(vibe, VibeType) else VibeType(vibe)
        suggested_dishes = VIBE_DISH_MAPPING.get(vibe_enum, [])

        for dish_name in suggested_dishes:
            if dish_name in seen_dishes:
                continue

            menu_item = menu_items_by_name.get(dish_name)
            if not menu_item:
                continue

            # Check dietary restrictions
            if vibe_data.dietary_restrictions:
                if "vegetarian" in vibe_data.dietary_restrictions and not menu_item.is_vegetarian:
                    continue
                if "vegan" in vibe_data.dietary_restrictions and not menu_item.is_vegan:
                    continue

            # Check allergies
            warnings = []
            if vibe_data.allergies:
                for allergen in menu_item.allergens:
                    if allergen.lower() in [a.lower() for a in vibe_data.allergies]:
                        warnings.append(f"Contains {allergen} - you indicated this allergy")

            # Check spice level
            if vibe_data.max_spice is not None and menu_item.spice_level:
                if menu_item.spice_level > vibe_data.max_spice:
                    continue

            seen_dishes.add(dish_name)

            recommendation = Recommendation(
                id=str(uuid4()),
                menu_item_id=menu_item.id,
                name=menu_item.name,
                reason=DISH_REASONS.get(dish_name, "A great choice based on your preferences."),
                match_score=0.85 + (0.1 * (1 - len(recommendations) * 0.02)),
                vibe_matches=[vibe_enum.value],
                price=menu_item.price,
                warnings=warnings,
                tags=menu_item.tags.copy(),
            )
            recommendations.append(recommendation)

    # If we don't have enough recommendations, add more from the menu
    if len(recommendations) < 3:
        for item in menu_data.items:
            if item.name in seen_dishes:
                continue
            if len(recommendations) >= 3:
                break

            recommendations.append(Recommendation(
                id=str(uuid4()),
                menu_item_id=item.id,
                name=item.name,
                reason="A popular choice from this restaurant.",
                match_score=0.70,
                vibe_matches=[],
                price=item.price,
                warnings=[],
                tags=item.tags.copy(),
            ))
            seen_dishes.add(item.name)

    # Build reasoning summary
    vibe_names = [v.value if isinstance(v, VibeType) else v for v in vibe_data.vibes]
    reasoning = f"Based on your {', '.join(vibe_names)} vibes"
    if vibe_data.party_size > 1:
        reasoning += f" for a party of {vibe_data.party_size}"
    reasoning += ", I've selected dishes that match your mood and preferences."

    recommendation_set = RecommendationSet(
        id=str(uuid4()),
        session_id=vibe_data.session_id,
        vibe_id=vibe_data.id,
        menu_id=menu_data.id,
        recommendations=recommendations[:5],  # Max 5 recommendations
        reasoning_summary=reasoning,
        confidence=0.88,
        generated_at=datetime.utcnow(),
        model_version="fake-v1",
    )

    return recommendation_set
