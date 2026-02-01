"""
Fake OCR service for MVP testing.
Returns predefined Thai menu items instead of actual OCR processing.
"""
from datetime import datetime
from typing import Optional
from uuid import uuid4

from app.models.domain import MenuItem, MenuData, Restaurant
from app.models.enums import ExtractionMethod


# Predefined fake Thai menu items
FAKE_MENU_ITEMS = [
    MenuItem(
        id=str(uuid4()),
        name="Pad Thai",
        description="Stir-fried rice noodles with eggs, tofu, bean sprouts, and peanuts in tamarind sauce",
        price=12.99,
        currency="USD",
        category="Noodles",
        tags=["popular", "signature"],
        allergens=["peanuts", "eggs", "soy"],
        spice_level=1,
        is_vegetarian=False,
        is_vegan=False,
        confidence=0.95,
    ),
    MenuItem(
        id=str(uuid4()),
        name="Green Curry",
        description="Creamy coconut curry with Thai basil, bamboo shoots, and your choice of protein",
        price=14.99,
        currency="USD",
        category="Curries",
        tags=["spicy", "creamy"],
        allergens=["coconut", "fish sauce"],
        spice_level=3,
        is_vegetarian=False,
        is_vegan=False,
        confidence=0.92,
    ),
    MenuItem(
        id=str(uuid4()),
        name="Tom Yum Soup",
        description="Hot and sour soup with lemongrass, galangal, lime leaves, and mushrooms",
        price=8.99,
        currency="USD",
        category="Soups",
        tags=["spicy", "healthy", "gluten-free"],
        allergens=["shellfish", "fish sauce"],
        spice_level=4,
        is_vegetarian=False,
        is_vegan=False,
        confidence=0.94,
    ),
    MenuItem(
        id=str(uuid4()),
        name="Mango Sticky Rice",
        description="Sweet glutinous rice with fresh mango slices and coconut cream",
        price=7.99,
        currency="USD",
        category="Desserts",
        tags=["sweet", "popular", "seasonal"],
        allergens=["coconut"],
        spice_level=0,
        is_vegetarian=True,
        is_vegan=False,
        confidence=0.97,
    ),
    MenuItem(
        id=str(uuid4()),
        name="Spring Rolls",
        description="Crispy vegetable spring rolls served with sweet chili sauce",
        price=6.99,
        currency="USD",
        category="Appetizers",
        tags=["vegetarian", "crispy", "sharing"],
        allergens=["gluten", "soy"],
        spice_level=0,
        is_vegetarian=True,
        is_vegan=True,
        confidence=0.96,
    ),
    MenuItem(
        id=str(uuid4()),
        name="Massaman Curry",
        description="Rich and mild curry with potatoes, onions, and roasted peanuts",
        price=15.99,
        currency="USD",
        category="Curries",
        tags=["mild", "comfort", "hearty"],
        allergens=["peanuts", "coconut", "fish sauce"],
        spice_level=1,
        is_vegetarian=False,
        is_vegan=False,
        confidence=0.91,
    ),
]

FAKE_RESTAURANT = Restaurant(
    name="Thai Orchid Kitchen",
    cuisine_type="Thai",
    address="123 Food Street, Culinary City",
)


async def process_menu_image(
    session_id: str,
    image_data: Optional[bytes] = None,
) -> MenuData:
    """
    Fake OCR processing that returns predefined menu items.
    In production, this would call Google Vision API.

    Args:
        session_id: The session ID for this menu extraction
        image_data: Optional image bytes (ignored in fake implementation)

    Returns:
        MenuData with fake Thai menu items
    """
    # Generate fresh IDs for each call
    items = []
    for item in FAKE_MENU_ITEMS:
        items.append(MenuItem(
            id=str(uuid4()),
            name=item.name,
            description=item.description,
            price=item.price,
            currency=item.currency,
            category=item.category,
            tags=item.tags.copy(),
            allergens=item.allergens.copy(),
            spice_level=item.spice_level,
            is_vegetarian=item.is_vegetarian,
            is_vegan=item.is_vegan,
            confidence=item.confidence,
        ))

    menu_data = MenuData(
        id=str(uuid4()),
        session_id=session_id,
        items=items,
        restaurant=FAKE_RESTAURANT,
        extraction_method=ExtractionMethod.OCR,
        confidence=0.94,
        extracted_at=datetime.utcnow(),
        raw_text="[Fake OCR text - Thai Orchid Kitchen Menu]",
        warnings=[],
    )

    return menu_data
