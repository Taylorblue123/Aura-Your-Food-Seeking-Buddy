"""
OCR service for menu extraction using OpenAI Vision API.
Falls back to fake data when OPENAI_API_KEY is not configured.
"""
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from app.core.config import settings
from app.models.enums import ExtractionMethod
from app.utils.errors import OCRFailedError

logger = logging.getLogger(__name__)


@dataclass
class MenuItem:
    """Represents a single menu item extracted from OCR."""
    id: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    currency: str = "USD"
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    allergens: List[str] = field(default_factory=list)
    spice_level: Optional[int] = None
    is_vegetarian: bool = False
    is_vegan: bool = False
    confidence: float = 1.0


@dataclass
class Restaurant:
    """Restaurant information extracted from menu."""
    name: Optional[str] = None
    cuisine_type: Optional[str] = None
    address: Optional[str] = None


@dataclass
class MenuData:
    """Complete menu data from OCR extraction."""
    id: str
    session_id: str
    items: List[MenuItem] = field(default_factory=list)
    restaurant: Optional[Restaurant] = None
    extraction_method: ExtractionMethod = ExtractionMethod.OCR
    confidence: float = 0.0
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    raw_text: Optional[str] = None
    warnings: List[str] = field(default_factory=list)


MENU_EXTRACTION_PROMPT = """You are a restaurant menu OCR extraction system. Extract ALL menu items visible in the image.

Return a JSON object with this exact structure:
{
  "restaurant": {
    "name": "restaurant name if visible, or null",
    "cuisine_type": "detected cuisine type, or null"
  },
  "items": [
    {
      "name": "dish name",
      "description": "dish description if available, or null",
      "price": 12.99,
      "currency": "USD",
      "category": "category like Appetizers, Mains, etc., or null",
      "tags": ["relevant tags like spicy, popular, etc."],
      "allergens": ["known allergens like peanuts, shellfish, etc."],
      "spice_level": null,
      "is_vegetarian": false,
      "is_vegan": false
    }
  ],
  "confidence": 0.85,
  "warnings": []
}

Rules:
- Extract EVERY item you can see, even if partially obscured
- If price is not visible, set to null
- Detect currency from context (symbols, country indicators)
- Infer allergens from ingredients when possible
- Set spice_level as 0-5 scale or null if unknown
- Mark confidence lower if image is blurry or text is hard to read
- If the image is not a menu, return {"items": [], "confidence": 0.0, "warnings": ["Image does not appear to be a restaurant menu"]}
- Menu may be in any language. Keep dish names EXACTLY as they appear on the menu. Do NOT translate or modify dish names. If a dish name is in Chinese, keep it in Chinese. Add an English translation in the "description" field if needed."""


async def _extract_with_openai(image_base64: str) -> dict:
    """Call OpenAI Vision API to extract menu items from image."""
    from app.services.openai_client import get_openai_client

    client = get_openai_client()

    logger.info("Calling OpenAI Vision API for menu extraction (image size: %d chars)", len(image_base64))
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": MENU_EXTRACTION_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all menu items from this restaurant menu image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "auto",
                        },
                    },
                ],
            },
        ],
        response_format={"type": "json_object"},
        timeout=60.0,
    )

    content = response.choices[0].message.content
    logger.info(
        "OCR complete — tokens: %s input, %s output",
        response.usage.prompt_tokens if response.usage else "?",
        response.usage.completion_tokens if response.usage else "?",
    )
    return json.loads(content)


def _parse_extraction(data: dict, session_id: str) -> MenuData:
    """Parse OpenAI JSON response into MenuData dataclass."""
    items = []
    for item_data in data.get("items", []):
        items.append(MenuItem(
            id=str(uuid4()),
            name=item_data.get("name", "Unknown"),
            description=item_data.get("description"),
            price=item_data.get("price"),
            currency=item_data.get("currency", "USD"),
            category=item_data.get("category"),
            tags=item_data.get("tags", []),
            allergens=item_data.get("allergens", []),
            spice_level=item_data.get("spice_level"),
            is_vegetarian=item_data.get("is_vegetarian", False),
            is_vegan=item_data.get("is_vegan", False),
            confidence=data.get("confidence", 0.5),
        ))

    restaurant_data = data.get("restaurant")
    restaurant = None
    if restaurant_data:
        restaurant = Restaurant(
            name=restaurant_data.get("name"),
            cuisine_type=restaurant_data.get("cuisine_type"),
        )

    warnings = data.get("warnings", [])
    confidence = data.get("confidence", 0.5)
    if confidence < 0.3:
        warnings.append("Low confidence extraction - results may be inaccurate")

    return MenuData(
        id=str(uuid4()),
        session_id=session_id,
        items=items,
        restaurant=restaurant,
        extraction_method=ExtractionMethod.OCR,
        confidence=confidence,
        extracted_at=datetime.utcnow(),
        raw_text=None,
        warnings=warnings,
    )


# --- Fallback fake data for dev mode (no API key) ---

FAKE_MENU_ITEMS = [
    MenuItem(id=str(uuid4()), name="Pad Thai", description="Stir-fried rice noodles with eggs, tofu, bean sprouts, and peanuts", price=12.99, category="Noodles", tags=["popular"], allergens=["peanuts", "eggs", "soy"], spice_level=1),
    MenuItem(id=str(uuid4()), name="Green Curry", description="Creamy coconut curry with Thai basil and bamboo shoots", price=14.99, category="Curries", tags=["spicy"], allergens=["coconut", "fish sauce"], spice_level=3),
    MenuItem(id=str(uuid4()), name="Tom Yum Soup", description="Hot and sour soup with lemongrass and mushrooms", price=8.99, category="Soups", tags=["spicy", "healthy"], allergens=["shellfish"], spice_level=4),
    MenuItem(id=str(uuid4()), name="Mango Sticky Rice", description="Sweet glutinous rice with fresh mango and coconut cream", price=7.99, category="Desserts", tags=["sweet"], allergens=["coconut"], spice_level=0, is_vegetarian=True),
    MenuItem(id=str(uuid4()), name="Spring Rolls", description="Crispy vegetable spring rolls with sweet chili sauce", price=6.99, category="Appetizers", tags=["vegetarian"], allergens=["gluten", "soy"], spice_level=0, is_vegetarian=True, is_vegan=True),
    MenuItem(id=str(uuid4()), name="Massaman Curry", description="Rich mild curry with potatoes, onions, and peanuts", price=15.99, category="Curries", tags=["mild", "comfort"], allergens=["peanuts", "coconut"], spice_level=1),
]


def _get_fake_menu(session_id: str) -> MenuData:
    """Return fake menu data for development without API key."""
    items = [
        MenuItem(id=str(uuid4()), name=i.name, description=i.description, price=i.price,
                 currency=i.currency, category=i.category, tags=list(i.tags),
                 allergens=list(i.allergens), spice_level=i.spice_level,
                 is_vegetarian=i.is_vegetarian, is_vegan=i.is_vegan, confidence=0.95)
        for i in FAKE_MENU_ITEMS
    ]
    return MenuData(
        id=str(uuid4()), session_id=session_id, items=items,
        restaurant=Restaurant(name="Thai Orchid Kitchen", cuisine_type="Thai"),
        extraction_method=ExtractionMethod.OCR, confidence=0.94,
        extracted_at=datetime.utcnow(), raw_text="[Fake OCR - dev mode]", warnings=[],
    )


async def process_menu_image(
    session_id: str,
    image_base64: str,
) -> MenuData:
    """
    Extract menu items from a photo using OpenAI Vision API.
    Falls back to fake data if OPENAI_API_KEY is not configured.

    Args:
        session_id: The session/device ID for this extraction
        image_base64: Base64-encoded image string

    Returns:
        MenuData with extracted menu items
    """
    if not settings.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set — returning fake menu data")
        return _get_fake_menu(session_id)

    try:
        data = await _extract_with_openai(image_base64)
        return _parse_extraction(data, session_id)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse OCR response JSON: %s", e)
        raise OCRFailedError(message="Failed to parse menu extraction results")
    except Exception as e:
        logger.error("OCR service error: %s", e)
        raise OCRFailedError(message=f"Menu extraction failed: {str(e)}")
