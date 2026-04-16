"""Inventory store — the main data container and operations layer."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator

from inventory.models import Product, Category


class InventoryStore:
    """In-memory inventory indexed by SKU.

    Design note: Products are stored in a dict keyed by SKU for O(1)
    lookups. The store is the single source of truth and provides all
    mutation methods so that business rules are enforced in one place.
    """

    def __init__(self) -> None:
        self._products: dict[str, Product] = {}

    # ── Core operations ──────────────────────────────────────────

    def add_product(self, product: Product) -> None:
        """Add a new product. Raises if SKU already exists."""
        if product.sku in self._products:
            raise KeyError(f"Product with SKU '{product.sku}' already exists")
        self._products[product.sku] = product

    def get_product(self, sku: str) -> Product | None:
        """Look up a product by SKU. Returns None if not found."""
        return self._products.get(sku)

    def remove_product(self, sku: str) -> Product:
        """Remove and return a product by SKU. Raises if not found."""
        if sku not in self._products:
            raise KeyError(f"No product with SKU '{sku}'")
        return self._products.pop(sku)

    def update_stock(self, sku: str, delta: int) -> None:
        """Adjust stock level for a product."""
        product = self.get_product(sku)
        if product is None:
            raise KeyError(f"No product with SKU '{sku}'")
        product.adjust_stock(delta)

    # ── Queries ──────────────────────────────────────────────────

    @property
    def count(self) -> int:
        """Total number of distinct products."""
        return len(self._products)

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[Product]:
        return iter(self._products.values())

    def __contains__(self, sku: str) -> bool:
        return sku in self._products

    def search(self, query: str) -> list[Product]:
        """Find products whose name contains the query (case-insensitive)."""
        query_lower = query.lower()
        return [p for p in self._products.values() if query_lower in p.name.lower()]

    def filter_by_category(self, category: Category) -> list[Product]:
        """Return all products in a given category."""
        return [p for p in self._products.values() if p.category == category]

    def low_stock_products(self) -> list[Product]:
        """Return products that are below the reorder threshold."""
        return [p for p in self._products.values() if p.is_low_stock]

    def total_inventory_value(self) -> float:
        """Sum of (quantity * price) across all products."""
        return sum(p.total_value for p in self._products.values())

    # ── Persistence ──────────────────────────────────────────────

    def load_csv(self, path: Path) -> int:
        """Load products from a CSV file. Returns count of products loaded.

        Skips rows that fail validation (e.g., negative quantity) and
        prints a warning instead of crashing the entire import.
        """
        loaded = 0
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    product = Product.from_dict(row)
                    self.add_product(product)
                    loaded += 1
                except (ValueError, KeyError) as e:
                    print(f"Warning: skipping invalid row {row}: {e}")
        return loaded

    def save_csv(self, path: Path) -> int:
        """Save all products to a CSV file. Returns count written."""
        if not self._products:
            return 0

        fieldnames = ["sku", "name", "quantity", "category", "price", "last_updated"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for product in self._products.values():
                writer.writerow(product.to_dict())
        return len(self._products)
