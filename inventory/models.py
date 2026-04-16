"""Domain models for the inventory system."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class Category(Enum):
    """Product categories in the warehouse."""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    TOOLS = "tools"
    OTHER = "other"

    @classmethod
    def from_string(cls, value: str) -> Category:
        """Parse a category from a string, falling back to OTHER."""
        try:
            return cls(value.lower().strip())
        except ValueError:
            return cls.OTHER


@dataclass
class Product:
    """A product in the warehouse inventory.

    Attributes:
        sku: Unique stock-keeping unit identifier.
        name: Human-readable product name.
        quantity: Number of items currently in stock.
        category: Product category.
        price: Unit price in DKK.
        last_updated: Timestamp of the last stock change.
    """
    sku: str
    name: str
    quantity: int
    category: Category
    price: float
    last_updated: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError(f"Quantity cannot be negative: {self.quantity}")
        if self.price < 0:
            raise ValueError(f"Price cannot be negative: {self.price}")
        if not self.sku:
            raise ValueError("SKU cannot be empty")

    @property
    def total_value(self) -> float:
        """Total value of this product's stock."""
        return self.quantity * self.price

    @property
    def is_low_stock(self) -> bool:
        """Whether stock is below the reorder threshold."""
        return self.quantity < 10

    def adjust_stock(self, delta: int) -> None:
        """Adjust stock by a positive or negative amount.

        Args:
            delta: Amount to add (positive) or remove (negative).

        Raises:
            ValueError: If adjustment would result in negative stock.
        """
        new_qty = self.quantity + delta
        if new_qty < 0:
            raise ValueError(
                f"Cannot remove {abs(delta)} units of '{self.name}' "
                f"(only {self.quantity} in stock)"
            )
        self.quantity = new_qty
        self.last_updated = datetime.now()

    def to_dict(self) -> dict:
        """Serialize to a dictionary for CSV/JSON export."""
        return {
            "sku": self.sku,
            "name": self.name,
            "quantity": self.quantity,
            "category": self.category.value,
            "price": self.price,
            "last_updated": self.last_updated.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Product:
        """Create a Product from a dictionary (e.g., CSV row)."""
        return cls(
            sku=data["sku"],
            name=data["name"],
            quantity=int(data["quantity"]),
            category=Category.from_string(data["category"]),
            price=float(data["price"]),
            last_updated=datetime.fromisoformat(data.get("last_updated", datetime.now().isoformat())),
        )
