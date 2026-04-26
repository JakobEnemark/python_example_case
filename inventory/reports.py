"""Report generation for inventory analysis."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory.store import InventoryStore


class ReportGenerator:
    """Generates summary reports from an InventoryStore.

    Separated from InventoryStore to keep reporting logic independent
    of storage logic (Single Responsibility Principle).
    """

    def __init__(self, store: InventoryStore) -> None:
        self._store = store

    def summary(self) -> dict:
        """High-level inventory summary."""
        return {
            "total_products": self._store.count,
            "total_value": round(self._store.total_inventory_value(), 2),
            "low_stock_count": len(self._store.low_stock_products()),
        }

    def category_breakdown(self) -> dict[str, int]:
        """Count of products per category."""
        counts: Counter[str] = Counter()
        for product in self._store:
            counts[product.category.value] += 1
        return dict(counts)

    def top_value_products(self, n: int = 5) -> list[dict]:
        """Return the top N products by total stock value."""
        products = sorted(self._store, key=lambda p: p.total_value, reverse=True)
        return [
            {"sku": p.sku, "name": p.name, "total_value": round(p.total_value, 2)}
            for p in products[:n]
        ]

    def format_text_report(self) -> str:
        """Format a human-readable text report."""
        s = self.summary()
        lines = [
            "=" * 50,
            "INVENTORY REPORT",
            "=" * 50,
            f"Total products: {s['total_products']}",
            f"Total value:    {s['total_value']:,.2f} DKK",
            f"Low stock:      {s['low_stock_count']} products",
            "",
            "Category breakdown:",
        ]

        for cat, count in sorted(self.category_breakdown().items()):
            lines.append(f"  {cat:<15} {count:>4}")

        lines.append("")
        lines.append("Top 5 by value:")
        for item in self.top_value_products(5):
            lines.append(f"  {item['sku']:<12} {item['name']:<25} {item['total_value']:>10,.2f} DKK")

        lines.append("=" * 50)
        return "\n".join(lines)


    def low_stock_report(self) -> str:
        
        low_products = self._store.low_stock_products()
    
        lines = [
            "LOW STOCK ALERT",
            "=" * 15,
        ]
    
        # If no low-stock products
        if not low_products:
            lines.append("All products are sufficiently stocked.")
            return "\n".join(lines)
    
        # Add each low-stock product
        for product in low_products:
            lines.append(
                f"{product.sku:<8} {product.name:<25} qty: {product.quantity}"
            )
    
        # Add footer
        lines.append("-" * 15)
        lines.append(
            f"Total: {len(low_products)} products need restocking"
        )
    
        return "\n".join(lines)
