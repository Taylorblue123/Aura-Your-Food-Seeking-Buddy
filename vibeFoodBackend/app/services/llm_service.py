"""
LLM recommendation service using OpenAI GPT-4o.
Falls back to hardcoded recommendations when OPENAI_API_KEY is not configured.
"""
import json
import logging
from typing import Dict, List, Optional

from app.core.config import settings
from app.utils.errors import LLMFailedError

logger = logging.getLogger(__name__)

VIBE_DESCRIPTIONS = {
    "comfort": "Warm, familiar, soul-satisfying food",
    "adventure": "Bold, unusual, exciting flavors",
    "light": "Fresh, not heavy, clean eating",
    "quick": "Fast to prepare, easy to eat",
    "sharing": "Good for groups, shareable portions",
    "budget": "Best value for money",
    "healthy": "Nutritious, balanced, wholesome",
    "indulgent": "Rich, decadent, treat-yourself food",
}

RECOMMENDATION_SYSTEM_PROMPT = """You are Aura, a friendly food recommendation assistant. Given a restaurant menu, a user's current mood (vibe), and their dietary preference, recommend 3-5 dishes.

Vibe meanings:
- comfort: Warm, familiar, soul-satisfying food
- adventure: Bold, unusual, exciting flavors
- light: Fresh, not heavy, clean eating
- quick: Fast to prepare, easy to eat
- sharing: Good for groups, shareable portions
- budget: Best value for money
- healthy: Nutritious, balanced, wholesome
- indulgent: Rich, decadent, treat-yourself food

Return a JSON object:
{
  "brief_summary": "One warm, personalized sentence about why these dishes match their vibe",
  "recommendations": [
    {
      "dish_name": "exact name from the menu",
      "reasoning": "Why this dish matches their vibe (1 sentence)",
      "story": "A brief, engaging description that makes the dish appealing (1 sentence)",
      "warnings": ["allergen or dietary warnings relevant to user's preference"],
      "price": "price as string from menu, or 'Ask staff' if unknown",
      "emoji": "single emoji that represents this dish"
    }
  ]
}

Rules:
- ONLY recommend dishes that appear on the provided menu
- Use the EXACT dish name as it appears in the menu data — do NOT translate, rephrase, or modify dish names
- The NUMBER of dishes to recommend should reflect the user's context:
  - If the user says they're alone, eating light, or just want a quick bite → recommend 1-2 dishes
  - If the user picks a standard vibe or gives no group size hint → recommend 3-4 dishes
  - If the user mentions a group, sharing, many people, or a big meal → recommend 4-6 dishes
  - Use common sense: "随便吃点" (just grab something) = 1-2, "人很多" (lots of people) = 5-6
- If user has dietary restrictions, ALWAYS flag conflicts in warnings
- If a dish conflicts with the user's dietary preference, you may still include it if it's an exceptional vibe match, but add a clear warning
- Price must match the menu price exactly
- Keep reasoning and story concise and warm in tone
- If the menu has very few items, recommend all that fit
- warnings should be null (not empty array) if there are no warnings
- CRITICAL: Write the brief_summary, reasoning, story, and warnings in the SAME LANGUAGE as the menu. If the menu language is "zh" (Chinese), write all text fields in Chinese. If "ja", write in Japanese. If "en" or unspecified, write in English. Dish names must remain exactly as they appear on the menu regardless of language."""


RESTAURANT_INTRO_PROMPT = """You are Gusto, a warm and friendly food companion. Given restaurant info extracted from a menu, write a 2-3 sentence introduction as if you're a friend telling someone about this place.

Rules:
- Be warm, specific, and make them excited to eat here
- Mention the cuisine style and what makes the menu interesting
- Never use star ratings, review counts, or review language
- Never say "I recommend" — save recommendations for later
- Keep it under 50 words
- Write in first person as Gusto talking to the user
- CRITICAL: You MUST write your response in the SAME LANGUAGE as the menu. If the menu language is "zh" (Chinese), write entirely in Chinese. If "ja", write in Japanese. If "en" or unspecified, write in English. Match the language the diners would read.

Return ONLY the introduction text, no JSON, no quotes."""


async def generate_restaurant_intro(
    restaurant_name: Optional[str],
    cuisine_type: Optional[str],
    categories: List[str],
    sample_items: List[str],
    menu_language: Optional[str] = None,
) -> Optional[str]:
    """
    Generate a warm 2-3 sentence restaurant intro using GPT-4o.
    Returns None if generation fails or API key not set.
    """
    if not settings.OPENAI_API_KEY:
        # Fallback template for dev mode
        name = restaurant_name or "This place"
        cuisine = f" {cuisine_type}" if cuisine_type else ""
        return f"{name} serves{cuisine} cuisine with a nice variety to explore. I think you'll find something great here!"

    try:
        from app.services.openai_client import get_openai_client
        client = get_openai_client()

        name = restaurant_name or "this restaurant"
        cuisine = cuisine_type or "varied"
        cats = ", ".join(categories[:5]) if categories else "various dishes"
        samples = ", ".join(sample_items[:6]) if sample_items else ""
        lang = menu_language or "en"

        user_msg = f"""Restaurant: {name}
Cuisine: {cuisine}
Menu sections: {cats}
Sample dishes: {samples}
Menu language: {lang}"""

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": RESTAURANT_INTRO_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            timeout=10.0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning("Restaurant intro generation failed: %s", e)
        return None


async def generate_recommendations(
    menu_items: List[Dict],
    vibe: str,
    preference: str,
    restaurant_info: Optional[Dict] = None,
    menu_language: Optional[str] = None,
    voice_prompt: Optional[str] = None,
) -> Dict:
    """
    Generate dish recommendations using GPT-4o.
    Falls back to hardcoded data if OPENAI_API_KEY is not set.

    Returns dict with "brief_summary" and "recommendations" keys.
    """
    if not settings.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set — returning fallback recommendations")
        return _get_fallback(vibe if vibe != "voice" else "comfort")

    try:
        return await _call_openai(menu_items, vibe, preference, restaurant_info, menu_language, voice_prompt)
    except Exception as e:
        logger.error("LLM recommendation error: %s", e)
        raise LLMFailedError(message=f"Recommendation generation failed: {str(e)}")


async def _call_openai(
    menu_items: list[dict],
    vibe: str,
    preference: str,
    restaurant_info: Optional[dict],
    menu_language: Optional[str] = None,
    voice_prompt: Optional[str] = None,
) -> dict:
    """Call OpenAI GPT-4o for recommendations."""
    from app.services.openai_client import get_openai_client

    client = get_openai_client()

    restaurant_context = ""
    if restaurant_info:
        name = restaurant_info.get("name", "Unknown")
        cuisine = restaurant_info.get("cuisine_type", "Unknown")
        restaurant_context = f"\nRestaurant: {name} ({cuisine} cuisine)"

    lang = menu_language or "en"
    menu_text = json.dumps(menu_items, indent=2, ensure_ascii=False)

    # Voice prompt overrides fixed vibe description
    if voice_prompt and vibe == "voice":
        vibe_line = f"User's request (in their own words): {voice_prompt}"
    else:
        vibe_line = f"User's vibe: {vibe} — {VIBE_DESCRIPTIONS.get(vibe, '')}"

    # Format preferences — may be comma-separated (e.g. "vegetarian,nut_free")
    pref_display = preference.replace(",", ", ") if preference else "no_restriction"

    user_message = f"""{vibe_line}
User's dietary restrictions: {pref_display}
Menu language: {lang}
{restaurant_context}

Menu items:
{menu_text}"""

    logger.info("Calling GPT-4o for recommendations (vibe=%s, preference=%s)", vibe, preference)
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": RECOMMENDATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
        timeout=20.0,
    )

    content = response.choices[0].message.content
    logger.info(
        "Recommendations complete — tokens: %s input, %s output",
        response.usage.prompt_tokens if response.usage else "?",
        response.usage.completion_tokens if response.usage else "?",
    )

    data = json.loads(content)

    # Validate that recommended dishes actually exist on the menu.
    # Use fuzzy matching: a dish is valid if the recommended name is a substring
    # of a menu name or vice versa (handles translated names, parenthetical
    # originals, and minor LLM rephrasing).
    menu_names = [item.get("name", "") for item in menu_items]
    valid_recs = []
    for rec in data.get("recommendations", []):
        rec_name = rec.get("dish_name", "")
        if _name_matches_menu(rec_name, menu_names):
            valid_recs.append(rec)
        else:
            logger.warning("LLM hallucinated dish: %s (not on menu)", rec_name)

    # If validation filtered everything out, the LLM likely used different
    # names than OCR. Return what we have rather than nothing.
    if not valid_recs:
        logger.warning("No valid recommendations after filtering — returning all from LLM")
        valid_recs = data.get("recommendations", [])

    data["recommendations"] = valid_recs
    return data


def _name_matches_menu(rec_name: str, menu_names: List[str]) -> bool:
    """Check if a recommended dish name matches any menu item name.

    Uses case-insensitive substring matching in both directions so that
    "Kung Pao Chicken" matches "Kung Pao Chicken (宫保鸡丁)" and
    "宫保鸡丁" matches "宫保鸡丁 Kung Pao Chicken".
    """
    rec_lower = rec_name.lower().strip()
    for menu_name in menu_names:
        menu_lower = menu_name.lower().strip()
        if rec_lower == menu_lower:
            return True
        if rec_lower in menu_lower or menu_lower in rec_lower:
            return True
    return False


# --- Fallback recommendations for dev mode ---

FALLBACK_RECOMMENDATIONS = {
    "comfort": {
        "brief_summary": "Here are some warming, comforting dishes to soothe your soul.",
        "recommendations": [
            {"dish_name": "Massaman Curry", "reasoning": "Rich and mild curry that feels like a warm hug", "story": "A comfort classic with tender meat and potatoes", "warnings": ["Contains peanuts - please verify with staff"], "price": "16", "emoji": "\U0001f35b"},
            {"dish_name": "Pad Thai", "reasoning": "A beloved classic with perfect sweet-savory balance", "story": "The most popular Thai dish for good reason", "warnings": ["Contains peanuts", "Contains eggs"], "price": "14", "emoji": "\U0001f35c"},
        ],
    },
    "adventure": {
        "brief_summary": "Ready for a flavor adventure? These dishes will excite your palate!",
        "recommendations": [
            {"dish_name": "Tom Yum Soup", "reasoning": "Bold flavors that awaken your taste buds", "story": "An exciting journey of sour, spicy, and aromatic notes", "warnings": ["Very spicy", "Contains shellfish"], "price": "12", "emoji": "\U0001f336\ufe0f"},
            {"dish_name": "Green Curry", "reasoning": "Aromatic and spicy with complex flavors", "story": "A Thai curry adventure with authentic heat", "warnings": ["Spicy", "Contains coconut"], "price": "15", "emoji": "\U0001f958"},
        ],
    },
    "light": {
        "brief_summary": "Light and refreshing options that won't weigh you down.",
        "recommendations": [
            {"dish_name": "Spring Rolls", "reasoning": "Fresh and crispy without being heavy", "story": "A light start that won't weigh you down", "warnings": None, "price": "7", "emoji": "\U0001f95f"},
            {"dish_name": "Tom Yum Soup", "reasoning": "Light broth-based soup full of fresh flavors", "story": "Refreshing and cleansing for the palate", "warnings": ["Spicy"], "price": "9", "emoji": "\U0001f372"},
        ],
    },
    "quick": {
        "brief_summary": "Fast favorites when you're short on time but not on taste.",
        "recommendations": [
            {"dish_name": "Pad Thai", "reasoning": "Quick to prepare and quick to enjoy", "story": "A fast favorite that never disappoints", "warnings": ["Contains peanuts"], "price": "14", "emoji": "\u26a1"},
            {"dish_name": "Spring Rolls", "reasoning": "Ready fast, perfect for a quick bite", "story": "Crispy satisfaction in minutes", "warnings": None, "price": "7", "emoji": "\U0001f95f"},
        ],
    },
    "sharing": {
        "brief_summary": "Perfect dishes for bringing the table together.",
        "recommendations": [
            {"dish_name": "Spring Rolls", "reasoning": "Perfect for passing around the table", "story": "A crowd-pleaser that brings people together", "warnings": None, "price": "7", "emoji": "\U0001f95f"},
            {"dish_name": "Pad Thai", "reasoning": "A generous portion great for sharing", "story": "Everyone's favorite to share", "warnings": ["Contains peanuts"], "price": "14", "emoji": "\U0001f35c"},
        ],
    },
    "budget": {
        "brief_summary": "Great taste without breaking the bank.",
        "recommendations": [
            {"dish_name": "Spring Rolls", "reasoning": "Great value without compromising taste", "story": "Budget-friendly and delicious", "warnings": None, "price": "7", "emoji": "\U0001f4b0"},
            {"dish_name": "Tom Yum Soup", "reasoning": "Filling and flavorful at a great price", "story": "Maximum flavor for minimum spend", "warnings": ["Spicy"], "price": "9", "emoji": "\U0001f372"},
        ],
    },
    "healthy": {
        "brief_summary": "Nutritious choices that don't sacrifice flavor.",
        "recommendations": [
            {"dish_name": "Tom Yum Soup", "reasoning": "Low calorie, high flavor, immune-boosting", "story": "A healthy choice packed with herbs and spices", "warnings": ["Spicy"], "price": "9", "emoji": "\U0001f957"},
            {"dish_name": "Spring Rolls", "reasoning": "Light and veggie-packed", "story": "Fresh vegetables in a light wrapper", "warnings": None, "price": "7", "emoji": "\U0001f96c"},
        ],
    },
    "indulgent": {
        "brief_summary": "Go ahead, treat yourself to these decadent delights.",
        "recommendations": [
            {"dish_name": "Mango Sticky Rice", "reasoning": "Sweet, creamy, and absolutely decadent", "story": "A heavenly dessert you deserve", "warnings": ["Contains coconut"], "price": "8", "emoji": "\U0001f96d"},
            {"dish_name": "Massaman Curry", "reasoning": "Rich, creamy, and deeply satisfying", "story": "Treat yourself to this indulgent curry", "warnings": ["Contains peanuts", "Contains coconut"], "price": "16", "emoji": "\U0001f35b"},
        ],
    },
}


def _get_fallback(vibe: str) -> dict:
    """Return fallback recommendations for dev mode."""
    return FALLBACK_RECOMMENDATIONS.get(vibe, FALLBACK_RECOMMENDATIONS["comfort"])
